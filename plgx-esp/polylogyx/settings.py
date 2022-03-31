# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from binascii import b2a_hex
import datetime as dt
import os

import pika

RABBITMQ_HOST = "localhost"
try:
    if os.environ.get('RABBITMQ_URL'):
        RABBITMQ_HOST = os.environ.get('RABBITMQ_URL')
except Exception as e:
    print(e)

credentials = pika.PlainCredentials("guest", "guest")


class Config(object):
    EMAIL_RECIPIENTS = []
    SECRET_KEY = b2a_hex(os.urandom(20))


    # Set the following to ensure Celery workers can construct an
    # external URL via `url_for`.
    # SERVER_NAME = "localhost:9000"
    SQLALCHEMY_POOL_SIZE = 30
    SQLALCHEMY_POOL_TIMEOUT = 300
    SQLALCHEMY_MAX_OVERFLOW = 20

    SERVER_PORT = 9000

    PREFERRED_URL_SCHEME = "https"
    CELERY_MAX_TASKS_PER_CHILD = 1
    # PREFERRED_URL_SCHEME will not work without SERVER_NAME configured,
    # so we need to use SSLify extension for that.
    # By default it is enabled for all production configs.
    ENFORCE_SSL = False

    DEBUG = False
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # When osquery is configured to start with the command-line flag
    # --host_identifier=uuid, set this value to True. This will allow
    # nodes requesting to enroll / re-enroll to reuse the same node_key.
    #
    # When set to False, nodes that request the /enroll endpoint subsequently
    # will have a new node_key generated, and a different corresponding
    # node record in the database. This will result in stale node entries.
    POLYLOGYX_EXPECTS_UNIQUE_HOST_ID = True
    POLYLOGYX_CHECKIN_INTERVAL = dt.timedelta(seconds=120)
    POLYLOGYX_ENROLL_OVERRIDE = 'enroll_secret'
    POLYLOGYX_PACK_DELIMITER = '/'
    POLYLOGYX_MINIMUM_OSQUERY_LOG_LEVEL = 0

    POLYLOGYX_ENROLL_SECRET_TAG_DELIMITER = None
    POLYLOGYX_ENROLL_DEFAULT_TAGS = [
    ]

    POLYLOGYX_CAPTURE_NODE_INFO = [
        ('computer_name', 'name'),
        ('hardware_vendor', 'make'),
        ('hardware_model', 'model'),
        ('hardware_serial', 'serial'),
        ('cpu_brand', 'cpu'),
        ('cpu_type', 'cpu type'),

        ('cpu_physical_cores', 'cpu cores'),
        ('physical_memory', 'memory'),
        ('mac', 'Mac address'),

    ]

    POLYLOGYX_CAPTURE_SHOW_INFO = [
        # ('computer_name', 'name'),
        # ('hardware_vendor', 'make'),
        # ('hardware_model', 'model'),
        # ('hardware_serial', 'serial'),
        # ('cpu_brand', 'cpu'),
        # ('cpu_physical_cores', 'cpu cores'),
        # ('physical_memory', 'memory'),
    ]

    # Doorman will validate queries against the expected set of tables from
    # osquery.  If you use any custom extensions, you'll need to add the
    # corresponding schema here so you can use them in queries.
    POLYLOGYX_EXTRA_SCHEMA = [
        'CREATE TABLE win_file_events(action TEXT, eid TEXT,target_path TEXT, md5 TEXT , sha256 TEXT, hashed BIGINT,uid TEXT, time BIGINT,utc_time TEXT, pe_file TEXT , pid BIGINT,process_guid TEXT , process_name TEXT);',
        'CREATE TABLE win_process_events(action TEXT, eid TEXT,pid BIGINT,process_guid TEXT , path TEXT ,cmdline TEXT,parent_pid BIGINT, parent_process_guid TEXT, parent_path TEXT,owner_uid TEXT, time BIGINT, utc_time TEXT  );',

        'CREATE TABLE win_process_open_events(action TEXT, eid TEXT,src_pid BIGINT,src_process_guid TEXT ,target_pid BIGINT,target_process_guid TEXT , src_path TEXT , target_path TEXT, granted_access TEXT, granted_access_value TEXT, owner_uid TEXT, time BIGINT, utc_time TEXT  );',
        'CREATE TABLE win_remote_thread_events( eid TEXT, action TEXT, src_pid BIGINT,src_process_guid TEXT ,target_pid BIGINT,target_process_guid TEXT , src_path TEXT ,target_path TEXT, function_name TEXT, module_name TEXT, owner_uid TEXT, time BIGINT, utc_time TEXT  );',

        'CREATE TABLE win_pefile_events(action TEXT, eid TEXT,target_path TEXT, md5 TEXT ,hashed BIGINT,uid TEXT, pid BIGINT,process_guid TEXT ,process_name TEXT, time BIGINT,utc_time TEXT );',
        'CREATE TABLE win_msr(turbo_disabled INTEGER , turbo_ratio_limt INTEGER ,platform_info INTEGER, perf_status INTEGER ,perf_ctl INTEGER,feature_control INTEGER, rapl_power_limit INTEGER ,rapl_energy_status INTEGER, rapl_power_units INTEGER );',
        'CREATE TABLE win_removable_media_events(action TEXT, eid TEXT,uid TEXT, pid BIGINT,time BIGINT, utc_time TEXT);',

        'CREATE TABLE win_http_events(event_type TEXT, action TEXT, eid TEXT, pid BIGINT,process_guid TEXT ,process_name TEXT, url TEXT, remote_address TEXT, remote_port BIGINT, time BIGINT,utc_time TEXT);',

        'CREATE TABLE win_epp_table(product_type TEXT, product_name TEXT,product_state TEXT, product_signatures TEXT);',

        'CREATE TABLE win_startup_items (name TEXT, path TEXT, args TEXT, type TEXT, source TEXT, status TEXT, username TEXT);',
        'CREATE TABLE win_services (name TEXT, service_type TEXT, display_name TEXT, status TEXT, pid INTEGER, start_type TEXT, win32_exit_code INTEGER, service_exit_code INTEGER, path TEXT, module_path TEXT, description TEXT, user_account TEXT);',
        'CREATE TABLE win_programs (name TEXT, version TEXT, install_location TEXT, install_source TEXT, language TEXT, publisher TEXT, uninstall_string TEXT, install_date TEXT, identifying_number TEXT);',

        'CREATE TABLE win_socket_events(event_type TEXT, eid TEXT, action TEXT, pid BIGINT,process_guid TEXT , process_name TEXT, family TEXT, protocol INTEGER, local_address TEXT, remote_address TEXT, local_port INTEGER,remote_port INTEGER, time BIGINT, utc_time TEXT);',
        'CREATE TABLE win_image_load_events(eid TEXT, pid BIGINT,process_guid TEXT ,uid TEXT,  image_path TEXT, sign_info TEXT, trust_info TEXT, time BIGINT, utc_time  \
    TEXT, num_of_certs BIGINT, cert_type \
        TEXT, version TEXT, pubkey TEXT, pubkey_length TEXT, pubkey_signhash_algo \
        TEXT, issuer_name TEXT, subject_name TEXT, serial_number TEXT, signature_algo \
    TEXT, subject_dn TEXT, issuer_dn TEXT);',
        'CREATE TABLE  win_yara_events( eid TEXT, target_path TEXT, category TEXT, action TEXT, matches TEXT, count INTEGER,md5 TEXT,time BIGINT, utc_time TEXT);',

        'CREATE TABLE  win_obfuscated_ps(script_id TEXT, time_created TEXT, obfuscated_state TEXT, obfuscated_score TEXT);',
        'CREATE TABLE  win_dns_events(event_type TEXT,eid TEXT, action TEXT, domain_name TEXT,request_type BIGINT,request_class BIGINT, pid TEXT, remote_address TEXT, remote_port BIGINT, time BIGINT, utc_time TEXT);',
        'CREATE TABLE win_dns_response_events( event_type TEXT,eid TEXT, action TEXT, domain_name TEXT,request_type BIGINT,request_class BIGINT,resolved_ip TEXT, pid BIGINT, remote_address TEXT, remote_port INTEGER , time BIGINT, utc_time TEXT  );',

        'CREATE TABLE  win_process_handles(pid BIGINT,process_guid TEXT , handle_type TEXT, object_name TEXT, access_mask BIGINT);',
        'CREATE TABLE  win_registry_events(action TEXT, eid TEXT, pid BIGINT,process_guid TEXT , process_name TEXT, target_name TEXT, target_new_name TEXT,value_data TEXT, value_type TEXT, owner_uid TEXT, time BIGINT, utc_time TEXT);',
        'CREATE TABLE win_file_timestomp_events(action TEXT, old_timestamp TEXT , new_timestamp TEXT, eid TEXT,target_path TEXT, md5 TEXT ,hashed BIGINT,uid TEXT, time BIGINT,utc_time TEXT, pe_file TEXT , pid BIGINT,process_guid TEXT , process_name TEXT);',

        'CREATE TABLE win_hash(sha1 TEXT, path TEXT,sha256 TEXT, md5 TEXT);',
        'CREATE TABLE win_image_load_process_map(pid BIGINT, process_guid TEXT , image_size TEXT, image_path TEXT,image_memory_mode TEXT, md5 TEXT ,image_base TEXT, time BIGINT,utc_time TEXT);',
        'CREATE TABLE win_mem_perf(physical_memory_load BIGINT, total_physical BIGINT,available_physical BIGINT, total_pagefile BIGINT,available_pagefile BIGINT, total_virtual TEXT, available_virtual BIGINT, available_extended_memory BIGINT);',
        'CREATE TABLE win_process_perf(name TEXT, pid BIGINT, user_time TEXT, privileged_time TEXT, processor_time TEXT, thread_count BIGINT, working_set TEXT, creating_process_id TEXT , elapsed_time TEXT, handle_count BIGINT, io_data_bytes_per_sec TEXT,  io_read_bytes_per_sec TEXT,io_read_ops_per_sec  TEXT, io_write_bytes_per_sec TEXT, io_write_ops_per_sec TEXT, non_paged_pool_bytes TEXT, page_pool_bytes_peak TEXT, priority_base TEXT, private_bytes TEXT, working_set_peak TEXT);',
        'CREATE TABLE win_logger_events(logger_name TEXT, logger_watch_file TEXT,log_entry TEXT);',
        'CREATE TABLE win_ssl_events(event_type TEXT, action TEXT,eid TEXT,subject_name TEXT, issuer_name TEXT,serial_number TEXT,dns_names TEXT, pid BIGINT,process_guid TEXT,process_name TEXT, remote_address TEXT,remote_port BIGINT, utc_time TEXT,time BIGINT);',

        'CREATE TABLE win_suspicious_process_dump(pid BIGINT, process_name TEXT,process_dumps_location TEXT);',
        'CREATE TABLE win_suspicious_process_scan(pid BIGINT, process_name TEXT, modules_scanned BIGINT,modules_suspicious BIGINT,modules_replaced BIGINT,modules_detached BIGINT,modules_hooked BIGINT,modules_implanted BIGINT,modules_skipped BIGINT,modules_errors BIGINT);',
        'CREATE TABLE win_yara( target_path TEXT,matches TEXT,count BIGINT,sig_group TEXT,sigfile TEXT);',
        'CREATE TABLE win_event_log_data(time BIGINT,datetime TEXT,source TEXT,provider_name TEXT,provider_guid TEXT,eventid BIGINT,task BIGINT,level BIGINT,keywords BIGINT,data TEXT,eid TEXT );',
        'CREATE TABLE win_event_log_channels(source TEXT );',




        'CREATE TABLE win_file_events_optimized(action TEXT, eid TEXT,target_path TEXT, md5 TEXT , sha256 TEXT, hashed BIGINT,uid TEXT, time BIGINT,utc_time TEXT, pe_file TEXT , pid BIGINT,process_guid TEXT , process_name TEXT);',
        'CREATE TABLE win_process_events_optimized(action TEXT, eid TEXT,pid BIGINT,process_guid TEXT , path TEXT ,cmdline TEXT,parent_pid BIGINT, parent_process_guid TEXT, parent_path TEXT,owner_uid TEXT, time BIGINT, utc_time TEXT  );',

        'CREATE TABLE win_process_open_events_optimized(action TEXT, eid TEXT,src_pid BIGINT,src_process_guid TEXT ,target_pid BIGINT,target_process_guid TEXT , src_path TEXT , target_path TEXT, granted_access TEXT, granted_access_value TEXT, owner_uid TEXT, time BIGINT, utc_time TEXT  );',
        'CREATE TABLE win_remote_thread_events_optimized( eid TEXT, action TEXT, src_pid BIGINT,src_process_guid TEXT ,target_pid BIGINT,target_process_guid TEXT , src_path TEXT ,target_path TEXT, function_name TEXT, module_name TEXT, owner_uid TEXT, time BIGINT, utc_time TEXT  );',

        'CREATE TABLE win_pefile_events_optimized(action TEXT, eid TEXT,target_path TEXT, md5 TEXT ,hashed BIGINT,uid TEXT, pid BIGINT,process_guid TEXT ,process_name TEXT, time BIGINT,utc_time TEXT );',
        'CREATE TABLE win_removable_media_events_optimized(action TEXT, eid TEXT,uid TEXT, pid BIGINT,time BIGINT, utc_time TEXT);',

        'CREATE TABLE win_http_events_optimized(event_type TEXT, action TEXT, eid TEXT, pid BIGINT,process_guid TEXT ,process_name TEXT, url TEXT, remote_address TEXT, remote_port BIGINT, time BIGINT,utc_time TEXT);',

        'CREATE TABLE win_socket_events_optimized(event_type TEXT, eid TEXT, action TEXT, pid BIGINT,process_guid TEXT , process_name TEXT, family TEXT, protocol INTEGER, local_address TEXT, remote_address TEXT, local_port INTEGER,remote_port INTEGER, time BIGINT, utc_time TEXT);',
        'CREATE TABLE win_image_load_events_optimized(eid TEXT, pid BIGINT,process_guid TEXT ,uid TEXT,  image_path TEXT, sign_info TEXT, trust_info TEXT, time BIGINT, utc_time  \
    TEXT, num_of_certs BIGINT, cert_type \
        TEXT, version TEXT, pubkey TEXT, pubkey_length TEXT, pubkey_signhash_algo \
        TEXT, issuer_name TEXT, subject_name TEXT, serial_number TEXT, signature_algo \
    TEXT, subject_dn TEXT, issuer_dn TEXT);',

        'CREATE TABLE  win_dns_events_optimized(event_type TEXT,eid TEXT, action TEXT, domain_name TEXT,request_type BIGINT,request_class BIGINT, pid TEXT, remote_address TEXT, remote_port BIGINT, time BIGINT, utc_time TEXT);',
        'CREATE TABLE win_dns_response_events_optimized( event_type TEXT,eid TEXT, action TEXT, domain_name TEXT,request_type BIGINT,request_class BIGINT,resolved_ip TEXT, pid BIGINT, remote_address TEXT, remote_port INTEGER , time BIGINT, utc_time TEXT  );',

        'CREATE TABLE  win_registry_events_optimized(action TEXT, eid TEXT, pid BIGINT,process_guid TEXT , process_name TEXT, target_name TEXT, target_new_name TEXT,value_data TEXT, value_type TEXT, owner_uid TEXT, time BIGINT, utc_time TEXT);',
        'CREATE TABLE win_file_timestomp_events_optimized(action TEXT, old_timestamp TEXT , new_timestamp TEXT, eid TEXT,target_path TEXT, md5 TEXT ,hashed BIGINT,uid TEXT, time BIGINT,utc_time TEXT, pe_file TEXT , pid BIGINT,process_guid TEXT , process_name TEXT);',

        'CREATE TABLE win_logger_events_optimized(logger_name TEXT, logger_watch_file TEXT,log_entry TEXT);',
        'CREATE TABLE win_ssl_events_optimized(event_type TEXT, action TEXT,eid TEXT,subject_name TEXT, issuer_name TEXT,serial_number TEXT,dns_names TEXT, pid BIGINT,process_guid TEXT,process_name TEXT, remote_address TEXT,remote_port BIGINT, utc_time TEXT,time BIGINT);',

    ]


    POLYLOGYX_OSQUERY_SCHEMA_JSON = {

    }
    CELERY_IMPORTS = ('polylogyx.tasks')
    CELERY_AMQP_TASK_RESULT_EXPIRES=60
    CELERY_TASK_RESULT_EXPIRES = 30
    CELERY_ROUTES = {
        'polylogyx.tasks.*': {'queue': 'worker1', 'routing_key': 'default1'},
    }
    CELERY_QUEUES = {
        "worker1": {"exchange": "default1", "binding_key": "default1"},
        "worker2": {"exchange": "default2", "binding_key": "default2"}
    }
    CELERY_CREATE_MISSING_QUEUES = True
    CELERY_DEFAULT_QUEUE = "worker1"

    CELERY_ACCEPT_CONTENT = ['djson', 'application/x-djson', 'application/json']
    CELERY_EVENT_SERIALIZER = 'djson'
    CELERY_RESULT_SERIALIZER = 'djson'
    CELERY_TASK_SERIALIZER = 'djson'
    # CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

    CELERYBEAT_SCHEDULE = {
        'alert-when-node-goes-offline': {
            'task': 'polylogyx.tasks.alert_when_node_goes_offline',
            'schedule': 10,
        },
    }
    # CELERY_TIMEZONE = 'Asia/Kolkata'
    # You can specify a set of custom logger plugins here.  These plugins will
    # be called for every status or result log that is received, and can
    # do what they wish with them.

    POLYLOGYX_LOG_PLUGINS = [
        # 'polylogyx.plugins.logs.file.LogPlugin',
        # 'polylogyx.plugins.logs.splunk.SplunkPlugin',
        'polylogyx.plugins.logs.rsyslog.RsyslogPlugin'
    ]

    POLYLOGYX_LOG_PLUGINS_OBJ = {
        "rsyslog": 'polylogyx.plugins.logs.rsyslog.RsyslogPlugin'
    }
    # These are the configuration variables for the example logger plugin given
    # above.  Uncomment these to start logging results or status logs to the
    # given file.
    POLYLOGYX_LOG_FILE_PLUGIN_JSON_LOG = '/tmp/osquery.log'  # Default: do not log status/results to json log
    POLYLOGYX_LOG_FILE_PLUGIN_STATUS_LOG = '/tmp/status.log'  # Default: do not log status logs
    POLYLOGYX_LOG_FILE_PLUGIN_RESULT_LOG = '/tmp/result.log'  # Default: do not log results
    POLYLOGYX_LOG_FILE_PLUGIN_APPEND = True  # Default: True

    # You can specify a set of alerting plugins here.  These plugins can be
    # configured in rules to trigger alerts to a particular location.  Each
    # plugin consists of a full path to be imported, combined with some
    # configuration for the plugin.  Note that, since an alerter can be
    # configured multiple times with different names, we provide the
    # configuration per-name.

    POLYLOGYX_THREAT_INTEL_PLUGINS = {
        'vtintel': ('polylogyx.plugins.intel.virustotal.VTIntel', {
            'level': 'error',
        }), 'ibmxforce': ('polylogyx.plugins.intel.ibmxforce.IBMxForceIntel', {
            'level': 'error',
        }), 'alienvault': ('polylogyx.plugins.intel.otx.OTXIntel', {
            'level': 'error',
        })
    }

    POLYLOGYX_ALERTER_PLUGINS = {
        'debug': ('polylogyx.plugins.alerters.debug.DebugAlerter', {
            'level': 'error',
        }),

        'rsyslog': ('polylogyx.plugins.alerters.rsyslog.RsyslogAlerter', {

            # Required
            'service_key': 'foobar',

            # Optional
            'client_url': 'https://polylogyx.domain.com',
            'key_format': 'polylogyx-security-{count}',
        }),

        'email': ('polylogyx.plugins.alerters.emailer.EmailAlerter', {
            # Required
            'recipients': [

            ],

            # Optional, see polylogyx/plugins/alerters/emailer.py for templates
            'subject_prefix': '[PolyLogyx]',
            'subject_template': 'email/alert.subject.txt',
            'message_template': 'email/alert.body.txt',

        }),

        # 'sentry': ('polylogyx.plugins.alerters.sentry.SentryAlerter', {
        #     'dsn': 'https://<key>:<secret>@app.getsentry.com/<project>',
        # }),

        # 'slack': ('polylogyx.plugins.alerters.slack.SlackAlerter', {
        #     # Required, create webhook here: https://my.slack.com/services/new/incoming-webhook/
        #     'slack_webhook' : 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX',

        #     # Optional
        #     'printColumns': False,
        #     'color': '#36a64f',
        # })
    }

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    # MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    MAIL_DEFAULT_SENDER = 'polylogyx@localhost'

    # PolyLogyx Fleet uses the WatchedFileHandler in logging.handlers module.
    # It is the responsibility of the system to rotate these logs on
    # a periodic basis, as the file will grow indefinitely. See
    # https://docs.python.org/dev/library/logging.handlers.html#watchedfilehandler
    # for more information.
    # Alternatively, you can set filename to '-' to log to stdout.

    POLYLOGYX_LOGGING_FILENAME = '-'
    POLYLOGYX_LOGGING_FORMAT = '%(asctime)s--%(levelname).1s--%(thread)d--%(funcName)s--%(message)s'
    POLYLOGYX_LOGGING_LEVEL = 'INFO'

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_DURATION = dt.timedelta(days=30)
    REMEMBER_COOKIE_PATH = '/manage'
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

    # see http://flask-login.readthedocs.io/en/latest/#session-protection
    # only applicable when POLYLOGYX_AUTH_METHOD = 'polylogyx'
    SESSION_PROTECTION = "strong"

    BCRYPT_LOG_ROUNDS = 13

    POLYLOGYX_AUTH_METHOD = None
    POLYLOGYX_AUTH_METHOD = 'polylogyx'
    # POLYLOGYX_AUTH_METHOD = 'google'
    # POLYLOGYX_AUTH_METHOD = 'ldap'

    POLYLOGYX_OAUTH_GOOGLE_ALLOWED_DOMAINS = [
    ]

    POLYLOGYX_OAUTH_GOOGLE_ALLOWED_USERS = [
    ]

    POLYLOGYX_OAUTH_CLIENT_ID = ''
    POLYLOGYX_OAUTH_CLIENT_SECRET = ''

    # When using POLYLOGYX_AUTH_METHOD = 'ldap', see
    # http://flask-ldap3-login.readthedocs.io/en/latest/configuration.html#core
    # Note: not all configuration options are documented at the link
    # provided above. A complete list of options can be groked by
    # reviewing the the flask-ldap3-login code.

    # LDAP_HOST = None
    # LDAP_PORT = 636
    # LDAP_USE_SSL = True
    # LDAP_BASE_DN = 'dc=example,dc=org'
    # LDAP_USER_DN = 'ou=People'
    # LDAP_GROUP_DN = ''
    # LDAP_USER_OBJECT_FILTER = '(objectClass=inetOrgPerson)'
    # LDAP_USER_LOGIN_ATTR = 'uid'
    # LDAP_USER_RDN_ATTR = 'uid'
    # LDAP_GROUP_SEARCH_SCOPE = 'SEARCH_SCOPE_WHOLE_SUBTREE'
    # LDAP_GROUP_OBJECT_FILTER = '(cn=*)(objectClass=groupOfUniqueNames)'
    # LDAP_GROUP_MEMBERS_ATTR = 'uniquemember'
    # LDAP_GET_GROUP_ATTRIBUTES = ['cn']
    # LDAP_OPT_X_TLS_CACERTFILE = None
    # LDAP_OPT_X_TLS_CERTIFICATE_FILE = None
    # LDAP_OPT_X_TLS_PRIVATE_KEY_FILE = None
    # LDAP_OPT_X_TLS_REQUIRE_CERT = 2  # ssl.CERT_REQUIRED
    # LDAP_OPT_X_TLS_USE_VERSION = 3  # ssl.PROTOCOL_TLSv1
    # LDAP_OPT_X_TLS_VALID_NAMES = []

    # To enable Sentry reporting, configure the following keys
    # https://docs.getsentry.com/hosted/clients/python/integrations/flask/
    # SENTRY_DSN = 'https://<key>:<secret>@app.getsentry.com/<project>'
    # SENTRY_INCLUDE_PATHS = ['polylogyx']
    # SENTRY_USER_ATTRS = ['username', 'first_name', 'last_name', 'email']
    #
    # https://docs.getsentry.com/hosted/clients/python/advanced/#sanitizing-data
    # SENTRY_PROCESSORS = [
    #     'raven.processors.SanitizePasswordsProcessor',
    # ]
    # RAVEN_IGNORE_EXCEPTIONS = []


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    ENFORCE_SSL = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://polylogyx:polylogyx@localhost:5432/polylogyx'

    try:
        SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.environ.get('POSTGRES_USER') + ':' + os.environ.get(
            'POSTGRES_PASSWORD') + '@' + os.environ.get('POSTGRES_ADDRESS') + ':' + os.environ.get(
            'POSTGRES_PORT') + '/' + os.environ.get('POSTGRES_DB_NAME')

    except:
        print('setting database address as localhost')
    POLYLOGYX_ENROLL_SECRET = [

    ]
    try:
        if os.environ['ENROLL_SECRET']:
            POLYLOGYX_ENROLL_SECRET = os.environ['ENROLL_SECRET'].split()
    except:
        print('Error in reading enroll secret')
    POLYLOGYX_MINIMUM_OSQUERY_LOG_LEVEL = 1
    try:
        BROKER_URL = 'pyamqp://guest:guest@' + os.environ.get('RABBITMQ_URL')
        CELERY_RESULT_BACKEND = 'rpc://'

    except Exception as e:
        print(e)


class DevConfig(Config):
    """
    This class specifies a configuration that is suitable for running in
    development.  It should not be used for running in production.
    """
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    ASSETS_DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://polylogyx:polylogyx@localhost:5432/polylogyx'

    POLYLOGYX_ENROLL_SECRET = [
        'secret',
    ]

    BROKER_URL = 'pyamqp://guest:guest@localhost//'
    CELERY_RESULT_BACKEND = 'rpc://'


class TestConfig(Config):
    """
    This class specifies a configuration that is used for our tests.
    """
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/polylogyx_test'

    WTF_CSRF_ENABLED = False

    POLYLOGYX_ENROLL_SECRET = [
        'secret',
    ]
    POLYLOGYX_EXPECTS_UNIQUE_HOST_ID = False

    POLYLOGYX_AUTH_METHOD = None


if os.environ.get('DYNO'):
    # we don't want to even define this class elsewhere,
    # because its definition depends on Heroku-specific environment variables
    class HerokuConfig(ProdConfig):
        """
        Environment variables accessed here are provided by Heroku.
        RABBITMQ_URL and DATABASE_URL are defined by addons,
        while others should be created using `heroku config`.
        They are also declared in `app.json`, so they will be created
        when deploying using `Deploy to Heroku` button.
        """
        ENV = 'heroku'

        POLYLOGYX_LOGGING_FILENAME = '-'  # handled specially - stdout

        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
        BROKER_URL = 'pyamqp://guest:guest@' + os.environ.get('RABBITMQ_URL')
        # CELERY_RESULT_BACKEND = 'pyamqp://guest:guest@'+os.environ.get('RABBITMQ_URL')
        CELERY_RESULT_BACKEND = "rpc://"

        try:
            SECRET_KEY = os.environ['SECRET_KEY']
        except KeyError:
            pass  # leave default random-filled key
        # several values can be specified as a space-separated string
        POLYLOGYX_ENROLL_SECRET = os.environ['ENROLL_SECRET'].split()

        POLYLOGYX_AUTH_METHOD = "google" if os.environ.get('OAUTH_CLIENT_ID') else None
        POLYLOGYX_OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID')
        POLYLOGYX_OAUTH_CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET')
        POLYLOGYX_OAUTH_GOOGLE_ALLOWED_USERS = os.environ.get('OAUTH_ALLOWED_USERS', '').split()

        # mail config
        MAIL_SERVER = os.environ.get('MAIL_SERVER')
        MAIL_PORT = os.environ.get('MAIL_PORT')
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
        MAIL_USE_SSL = True

        POLYLOGYX_ALERTER_PLUGINS = {
            'debug': ('polylogyx.plugins.alerters.debug.DebugAlerter', {
                'level': 'error',
            }),
            'rsyslog': ('polylogyx.plugins.alerters.rsyslog.RsyslogAlerter', {

                'service_key': 'foobar',

                # Optional
                'client_url': 'https://polylogyx.domain.com',
                'key_format': 'polylogyx-security-{count}',
            }),
            'email': ('polylogyx.plugins.alerters.emailer.EmailAlerter', {
                'recipients': [
                    email.strip() for email in
                    os.environ.get('MAIL_RECIPIENTS', '').split(';')
                ],
            }),

        }

# choose proper configuration based on environment -
# this is both for manage.py and for worker.py
if os.environ.get('POLYLOGYX_ENV') == 'prod':
    CurrentConfig = ProdConfig
elif os.environ.get('POLYLOGYX_ENV') == 'test':
    CurrentConfig = TestConfig
elif os.environ.get('DYNO'):
    CurrentConfig = HerokuConfig
else:
    CurrentConfig = DevConfig
