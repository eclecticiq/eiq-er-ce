# -*- coding: utf-8 -*-
import datetime as dt
import json, os, sqlite3, ast, string, threading, pkg_resources, requests, six
from collections import namedtuple
from functools import wraps

from operator import itemgetter
from os.path import basename, join, splitext
from sqlalchemy import and_, or_

from flask_mail import Message, Mail
from flask import current_app, flash, request, abort, jsonify, g


from polylogyx.constants import PolyLogyxServerDefaults, DEFAULT_PLATFORMS
from polylogyx.database import db
from polylogyx.models import (
    DistributedQuery, DistributedQueryTask, HandlingToken,
    Node, Pack, Query, ResultLog, querypacks,
    Options, Settings, AlertEmail, Tag, User, DefaultFilters, DefaultQuery, Config)

Field = namedtuple('Field', ['name', 'action', 'columns', 'timestamp'])

# Read DDL statements from our package
schema = pkg_resources.resource_string('polylogyx', join('resources', 'osquery_schema.sql'))
schema = schema.decode('utf-8')
schema = [x for x in schema.strip().split('\n') if not x.startswith('--')]

# SQLite in Python will complain if you try to use it from multiple threads.
# We create a threadlocal variable that contains the DB, lazily initialized.
osquery_mock_db = threading.local()


def send_test_mail(settings):
    from flask import Flask
    test_app = Flask(__name__)
    test_app.config['EMAIL_RECIPIENTS'] = settings['emailRecipients']
    test_app.config['MAIL_USERNAME'] = settings['email']
    test_app.config['MAIL_PASSWORD'] = settings['password']
    test_app.config['MAIL_SERVER'] = settings['smtpAddress']
    test_app.config['MAIL_PORT'] = int(settings.get('smtpPort', 465))
    test_app.config['MAIL_USE_SSL'] = settings['use_ssl']
    test_app.config['MAIL_USE_TLS'] = settings['use_tls']

    content = """Test message"""
    subject = "Sent from PolyLogyx-ESP"
    return send_mail(test_app, content, subject)


def send_mail(app, content, subject):
    import socket
    socket.setdefaulttimeout(30)
    if app.config['EMAIL_RECIPIENTS']:
        message = Message(
            subject.strip(),
            sender=app.config['MAIL_USERNAME'],
            recipients=app.config['EMAIL_RECIPIENTS'],
            body=content,
            charset='utf-8',
        )
        mail = Mail(app=app)
        try:
            mail.send(message)
            return True
        except Exception as e:
            current_app.logger.error("Unable to send mail - {}".format(str(e)))
    return False


def assemble_additional_configuration(node):
    configuration = {}
    configuration['queries'] = assemble_queries(node)
    configuration['packs'] = assemble_packs(node)
    configuration['tags'] = [tag.value for tag in node.tags]
    configuration=merge_two_dicts(configuration,assemble_filters(node))
    return configuration


def assemble_configuration(node):
    configuration = {}
    configuration['options'] = assemble_options(node)
    configuration['file_paths'] = assemble_file_paths(node)
    configuration['queries'] = assemble_schedule(node)
    configuration['packs'] = assemble_packs(node)
    configuration['filters'] = assemble_filters(node)
    return configuration


def get_additional_config(node):
    configuration = {}
    configuration['queries'] = assemble_schedule(node)
    configuration['packs'] = assemble_packs(node)
    configuration['tags'] = [tag.value for tag in node.tags]
    return configuration


def assemble_options(node):
    options = {}

    # https://github.com/facebook/osquery/issues/2048#issuecomment-219200524
    options['disable_watchdog'] = True
    options['logger_tls_compress'] = True
    if current_app.config['POLYLOGYX_EXPECTS_UNIQUE_HOST_ID']:
        options['host_identifier'] = 'uuid'
    else:
        options['host_identifier'] = 'hostname'

    options['schedule_splay_percent'] = 10
    existing_option = Options.query.filter(Options.name == PolyLogyxServerDefaults.plgx_config_all_options).first()
    if existing_option:
        existing_option_value = json.loads(existing_option.option)
        options = merge_two_dicts(options, existing_option_value)
    return options


def assemble_file_paths(node):
    file_paths = {}
    for file_path in node.file_paths.options(db.lazyload('*')):
        file_paths.update(file_path.to_dict())
    return file_paths


def assemble_queries(node, config_json=None):
    if config_json:
        schedule = {}
        for query in node.queries.options(db.lazyload('*')):
            schedule[query.name] = query.to_dict()
        if config_json:
            schedule = merge_two_dicts(schedule, config_json.get('schedule'))
    else:
        schedule=[]
        for query in node.queries.options(db.lazyload('*')):
            schedule.append(query.to_dict())
    return schedule


def assemble_schedule(node):
    schedule = {}
    for query in node.queries.options(db.lazyload('*')):
        schedule[query.name] = query.to_dict()
    platform = node.platform
    if platform not in DEFAULT_PLATFORMS:
        platform = 'linux'
    is_x86 = False
    if node.node_info and 'cpu_type' in node.node_info and node.node_info['cpu_type'] == DefaultQuery.ARCH_x86:
        is_x86 = True

    query = db.session.query(DefaultQuery).join(Config).filter(Config.is_active == True).filter(
        DefaultQuery.platform == platform).filter(DefaultQuery.status == True)
    if is_x86:
        queries = query.filter(DefaultQuery.arch == DefaultQuery.ARCH_x86).all()
    else:
        queries = query.filter(
            or_(DefaultQuery.arch == None, DefaultQuery.arch != DefaultQuery.ARCH_x86)).all()

    for default_query in queries:
        schedule[default_query.name] = default_query.to_dict()

    return schedule


def assemble_packs(node, config_json=None):
    if config_json:
        packs = {}
        for pack in node.packs.join(querypacks).join(Query) \
                .options(db.contains_eager(Pack.queries)).all():
            packs[pack.name] = pack.to_dict()
        if config_json:
            packs = merge_two_dicts(packs, config_json.get('packs'))
    else:
        packs = []
        for pack in node.packs.join(querypacks).join(Query) \
                .options(db.contains_eager(Pack.queries)).all():
            packs.append(pack.to_dict())
    return packs


def assemble_distributed_queries(node):
    '''
    Retrieve all distributed queries assigned to a particular node
    in the NEW state. This function will change the state of the
    distributed query to PENDING, however will not commit the change.
    It is the responsibility of the caller to commit or rollback on the
    current database session.
    '''
    now = dt.datetime.utcnow()
    pending_query_count = 0
    query_recon_count = db.session.query(db.func.count(DistributedQueryTask.id)) \
        .filter(
        DistributedQueryTask.node == node,
        DistributedQueryTask.status == DistributedQueryTask.NEW,
        DistributedQueryTask.priority == DistributedQueryTask.HIGH,

    )
    for r in query_recon_count:
        pending_query_count = r[0]
    if pending_query_count > 0:
        query = db.session.query(DistributedQueryTask) \
            .join(DistributedQuery) \
            .filter(
            DistributedQueryTask.node == node,
            DistributedQueryTask.status == DistributedQueryTask.NEW,
            DistributedQuery.not_before < now,
            DistributedQueryTask.priority == DistributedQueryTask.HIGH,

        ).options(
            db.lazyload('*'),
            db.contains_eager(DistributedQueryTask.distributed_query)
        )
    else:
        query = db.session.query(DistributedQueryTask) \
            .join(DistributedQuery) \
            .filter(
            DistributedQueryTask.node == node,
            DistributedQueryTask.status == DistributedQueryTask.NEW,
            DistributedQuery.not_before < now,
            DistributedQueryTask.priority == DistributedQueryTask.LOW,
        ).options(
            db.lazyload('*'),
            db.contains_eager(DistributedQueryTask.distributed_query)
        ).limit(1)

    queries = {}
    for task in query:
        if task.sql:
            queries[task.guid] = task.sql
        else:
            queries[task.guid] = task.distributed_query.sql
        task.update(status=DistributedQueryTask.PENDING,
                    timestamp=now,
                    commit=False)

        # add this query to the session, but don't commit until we're
        # as sure as we possibly can be that it's been received by the
        # osqueryd client. unfortunately, there are no guarantees though.
        db.session.add(task)
    return queries


def assemble_filters(node):
    platform = node.platform
    if platform not in DEFAULT_PLATFORMS:
        platform = 'linux'
    is_x86 = False
    if node.node_info and 'cpu_type' in node.node_info and node.node_info['cpu_type'] == DefaultFilters.ARCH_x86:
        is_x86 = True
    query = DefaultFilters.query.filter(DefaultFilters.platform == platform).join(Config).filter(Config.is_active == True)

    if is_x86:
        default_filters_obj=query.filter(DefaultFilters.arch == DefaultFilters.ARCH_x86).first()
    else:
        default_filters_obj=query.filter(
            and_(DefaultFilters.arch != DefaultFilters.ARCH_x86)).first()
    if default_filters_obj:
        return default_filters_obj.filters


def create_tags(*tags):
    values = []
    existing = []

    # create a set, because we haven't yet done our association_proxy in
    # sqlalchemy

    for value in (v.strip() for v in set(tags) if v.strip()):
        tag = Tag.query.filter(Tag.value == value).first()
        if not tag:
            values.append(Tag.create(value=value))
        else:
            existing.append(tag)
    else:
        if values:
            flash(u"Created tag{0} {1}".format(
                's' if len(values) > 1 else '',
                ', '.join(tag.value for tag in values)),
                'info')
    return values + existing


def get_tags(*tags):
    values = []
    existing = []

    # create a set, because we haven't yet done our association_proxy in
    # sqlalchemy

    for value in (v.strip() for v in set(tags) if v.strip()):
        tag = Tag.query.filter(Tag.value == value).first()
        if tag:
            existing.append(tag)
    return existing


def merge_two_dicts(x, y):
    if not x:
        x = {}
    if not y:
        y = {}
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z


def get_node_health(node):
    checkin_interval = current_app.config['POLYLOGYX_CHECKIN_INTERVAL']
    if isinstance(checkin_interval, (int, float)):
        checkin_interval = dt.timedelta(seconds=checkin_interval)
    if (dt.datetime.utcnow() - node.last_checkin) > checkin_interval:
        return u'danger'
    else:
        return ''


# Not super-happy that we're duplicating this both here and in the JS, but I
# couldn't think of a nice way to pass from JS --> Python (or the other
# direction).
PRETTY_OPERATORS = {
    'equal': 'equals',
    'not_equal': "doesn't equal",
    'begins_with': 'begins with',
    'not_begins_with': "doesn't begins with",
    'contains': 'contains',
    'not_contains': "doesn't contain",
    'ends_with': 'ends with',
    'not_ends_with': "doesn't end with",
    'is_empty': 'is empty',
    'is_not_empty': 'is not empty',
    'less': 'less than',
    'less_or_equal': 'less than or equal',
    'greater': 'greater than',
    'greater_or_equal': 'greater than or equal',
    'matches_regex': 'matches regex',
    'not_matches_regex': "doesn't match regex",
}



PRETTY_FIELDS = {
    'query_name': 'Query name',
    'action': 'Action',
    'host_identifier': 'Host identifier',
    'timestamp': 'Timestamp',
}



# Since 'string.printable' includes control characters
PRINTABLE = string.ascii_letters + string.digits + string.punctuation + ' '


def quote(s, quote='"'):
    buf = [quote]
    for ch in s:
        if ch == quote or ch == '\\':
            buf.append('\\')
            buf.append(ch)
        elif ch == '\n':
            buf.append('\\n')
        elif ch == '\r':
            buf.append('\\r')
        elif ch == '\t':
            buf.append('\\t')
        elif ch in PRINTABLE:
            buf.append(ch)
        else:
            # Hex escape
            buf.append('\\x')
            buf.append(hex(ord(ch))[2:])

    buf.append(quote)
    return ''.join(buf)


def _carve(string):
    return str(string).title()


def create_mock_db():
    mock_db = sqlite3.connect(':memory:')
    mock_db.create_function("carve", 1, _carve)

    for ddl in schema:
        mock_db.execute(ddl)
    cursor = mock_db.cursor()
    cursor.execute("SELECT name,sql FROM sqlite_master WHERE type='table';")
    from polylogyx.constants import PolyLogyxServerDefaults

    extra_schema = current_app.config.get('POLYLOGYX_EXTRA_SCHEMA', [])
    optimized_extra_schema = current_app.config.get('POLYLOGYX_EXTRA_SCHEMA_OPTIMIZED', [])
    if optimized_extra_schema and not optimized_extra_schema[0] in extra_schema:
        extra_schema.extend(optimized_extra_schema)
    for ddl in extra_schema:
        mock_db.execute(ddl)
    for osquery_table in cursor.fetchall():
        PolyLogyxServerDefaults.POLYLOGYX_OSQUERY_SCHEMA_JSON[osquery_table[0]] = osquery_table[1]
    return mock_db


def validate_osquery_query(query):
    # Check if this thread has an instance of the SQLite database
    db = getattr(osquery_mock_db, 'db', None)
    if db is None:
        db = create_mock_db()
        osquery_mock_db.db = db

    try:
        db.execute(query)
    except sqlite3.Error:
        current_app.logger.exception("Invalid query: %s", query)
        return False
    except sqlite3.Warning:
        current_app.logger.exception("Invalid query: %s Only one query can be executed a time!", query)
        return False

    return True


def learn_from_result(result, node):
    if not result['data']:
        return

    capture_columns = set(
        map(itemgetter(0),
            current_app.config['POLYLOGYX_CAPTURE_NODE_INFO']
            )
    )

    if not capture_columns:
        return

    node_info = node.get('node_info', {})
    orig_node_info = node_info.copy()

    for _, action, columns, _, in extract_results(result):
        # only update columns common to both sets
        for column in capture_columns & set(columns):

            cvalue = node_info.get(column)  # current value
            value = columns.get(column)

            if action == 'removed' and (cvalue is None or cvalue != value):
                pass
            elif action == 'removed' and cvalue == value:
                node_info.pop(column)
            elif action == 'added' and (cvalue is None or cvalue != value):
                node_info[column] = value

    # only update node_info if there's actually a change

    if orig_node_info == node_info:
        return

    node = Node.get_by_id(node['id'])
    node.update(node_info=node_info)
    return


def process_result(result, node):
    if not result['data']:
        current_app.logger.error("No results to process from %s", node)
        return
    subject_dn = []
    for name, action, columns, timestamp, in extract_results(result):
        if 'subject_dn' in columns and columns['subject_dn'] and columns['subject_dn'] != '':
            subject_dn.append(columns['subject_dn'])
        yield ResultLog(name=name,
                        action=action,
                        columns=columns,
                        timestamp=timestamp,
                        node_id=node.id)


def extract_results(result):
    """
    extract_results will convert the incoming log data into a series of Fields,
    normalizing and/or aggregating both batch and event format into batch
    format, which is used throughout the rest of polylogyx.
    """
    if not result['data']:
        return

    timefmt = '%a %b %d %H:%M:%S %Y UTC'
    strptime = dt.datetime.strptime

    for entry in result['data']:
        name = entry['name']
        timestamp = strptime(entry['calendarTime'], timefmt)

        if 'columns' in entry:
            yield Field(name=name,
                        action=entry['action'],
                        columns=entry['columns'],
                        timestamp=timestamp)

        elif 'diffResults' in entry:
            added = entry['diffResults']['added']
            removed = entry['diffResults']['removed']
            for (action, items) in (('added', added), ('removed', removed)):
                # items could be "", so we're still safe to iter over
                # and ensure we don't return an empty value for columns
                for columns in items:
                    yield Field(name=name,
                                action=action,
                                columns=columns,
                                timestamp=timestamp)

        elif 'snapshot' in entry:
            for columns in entry['snapshot']:
                yield Field(name=name,
                            action='snapshot',
                            columns=columns,
                            timestamp=timestamp)

        else:
            current_app.logger.error("Encountered a result entry that "
                                     "could not be processed! %s",
                                     json.dumps(entry))


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, dt.datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def is_token_logged_out(loggedin_token):
    qs_object = HandlingToken.query.filter(HandlingToken.token == loggedin_token).first()
    if qs_object and qs_object.token_expired:
        return True
    elif qs_object:
        return False
    return


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if User.verify_auth_token(request.headers.environ.get('HTTP_X_ACCESS_TOKEN')) and is_token_logged_out(request.headers.environ.get('HTTP_X_ACCESS_TOKEN')) is False:
            return f(*args, **kwargs)
        elif request.path.endswith('swagger.json'):
            return f(*args, **kwargs)
        elif User.is_auth_token_exists(request.headers.environ.get('HTTP_X_ACCESS_TOKEN')) or is_token_logged_out(request.headers.environ.get('HTTP_X_ACCESS_TOKEN')):
            return abort(401, {'message': 'This API key used to authenticate is expired!'})
        else:
            current_app.logger.error("%s - Request did not contain valid API key", request.remote_addr)
            return abort(401, {'message': 'Request did not contain valid API key!'})

    return decorated_function


def is_number_positive(number=None):
    if number>0:
        return True
    else: return False
