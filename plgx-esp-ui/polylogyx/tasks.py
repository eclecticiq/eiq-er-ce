# -*- coding: utf-8 -*-
import base64

import datetime as dt
import sqlalchemy
from celery import Celery
from flask import current_app, json
from kombu import Exchange, Queue

from polylogyx.models import Settings, AlertEmail, Node, ResultLog, StatusLog, db, Alerts, CarveSession, DistributedQueryTask
from polylogyx.constants import PolyLogyxServerDefaults

celery = Celery(__name__)
default_exchange = Exchange('default', type='direct')

celery.conf.task_queues = (
    Queue('worker3', default_exchange, routing_key='default'),
)
celery.conf.task_default_queue = 'worker3'
celery.conf.task_default_exchange = 'default'
celery.conf.task_default_routing_key = 'default'
celery.conf.beat_schedule = {
    "send-alert-emails": {
        "task": "polylogyx.tasks.send_alert_emails",
        "schedule": 86400.0
    }, "purge_old_data": {
        "task": "polylogyx.tasks.purge_old_data",
        "schedule": 86400.0
    }
}


def update_sender_email(db):
    email_sender_obj = db.session.query(Settings).filter(
        Settings.name == PolyLogyxServerDefaults.plgx_config_all_settings).first()
    if not email_sender_obj:
        current_app.logger.info("Email credentials are not set..")
        return False
    try:
        settings = json.loads(email_sender_obj.setting)
        current_app.config['EMAIL_RECIPIENTS'] = settings['emailRecipients']
        current_app.config['MAIL_USERNAME'] = settings['email']
        current_app.config['MAIL_PASSWORD'] = base64.decodestring(settings['password'].encode('utf-8')).decode('utf-8')
        current_app.config['MAIL_SERVER'] = settings['smtpAddress']
        current_app.config['MAIL_PORT'] = int(settings['smtpPort'])
        current_app.config['MAIL_USE_SSL'] = settings['use_ssl']
        current_app.config['MAIL_USE_TLS'] = settings['use_tls']
        return True
    except Exception as e:
        current_app.logger.info("Incomplete email credentials")
        current_app.logger.error(e)
        return False


@celery.task()
def send_alert_emails():
    from polylogyx.models import db
    current_app.logger.info("Task is started to send the pending emails of the alerts reported")
    email_credentials_valid = update_sender_email(db)
    if email_credentials_valid:
        nodes = Node.query.all()
        for node in nodes:
            try:
                send_pending_node_emails(node, db)
                current_app.logger.info("Pending emails of the alerts reported are sent")
            except Exception as e:
                current_app.logger.error(e.message)
    current_app.logger.info("Task is completed in sending the pending emails of the alerts reported")


def send_pending_node_emails(node, db):
    from polylogyx.utils import send_mail
    alert_emails = AlertEmail.query.filter(AlertEmail.node == node).filter(AlertEmail.status == None).all()
    body = ''
    is_mail_sent = False
    for alert_email in alert_emails:
        body = body + alert_email.body
    if body:
        db.session.query(AlertEmail).filter(AlertEmail.status == None).filter(AlertEmail.node == node).update(
            {'status': 'PENDING'})
        db.session.commit()
        try:
            is_mail_sent = send_mail(app=current_app, content=body, subject=node.display_name + ' Alerts Today')
        except Exception as e:
            current_app.logger.error(e.message)
        if is_mail_sent:
            db.session.query(AlertEmail).filter(AlertEmail.status == 'PENDING').filter(
                AlertEmail.node == node).update(
                {'status': 'COMPLETED'})
        else:
            db.session.query(AlertEmail).filter(AlertEmail.status == 'PENDING').filter(
                AlertEmail.node == node).update(
                {'status': None})
        db.session.commit()


@celery.task()
def purge_old_data():
    from polylogyx import db
    import time, datetime
    current_app.logger.info("Task to purge older data is started")
    try:
        deleted_hosts = Node.query.filter(Node.state == Node.DELETED).all()
        node_ids_to_delete = [node.id for node in deleted_hosts if not node.result_logs.count() and not node.status_logs.count()]
        if node_ids_to_delete:
            permanent_host_deletion.apply_async(queue='default_queue_ui_tasks', args=[node_ids_to_delete])

        delete_setting = db.session.query(Settings).filter(Settings.name == 'purge_data_duration').first()
        current_app.logger.info("Purging the data for the duration {}".format(int(delete_setting.setting)))
        max_delete_count = 1000
        actual_delete_count = 1000
        if delete_setting and int(delete_setting.setting) > 0:
            since = dt.datetime.now() - dt.timedelta(hours=24 * int(delete_setting.setting))
            while actual_delete_count == 1000:
                try:
                    actual_delete_count = int(ResultLog.query.filter(ResultLog.id.in_(db.session.query(ResultLog.id).filter(ResultLog.timestamp < since).limit(max_delete_count))).delete(synchronize_session='fetch'))
                    db.session.commit()
                    current_app.logger.info("Purged {0} records".format(actual_delete_count))
                    time.sleep(2)
                except Exception as e:
                    db.session.commit()
                    current_app.logger.error("Error in Purge : {0}".format(e))

            current_app.logger.info("Purging the Status Logs beyond the purge duration")
            StatusLog.query.filter(StatusLog.created < since).delete()
            db.session.commit()

            current_app.logger.info("Purging the Alerts beyond the purge duration")
            Alerts.query.filter(Alerts.created_at < since).delete()
            db.session.commit()

            hosts = db.session.query(Node.host_identifier, Node.id).filter(Node.state == Node.DELETED).filter(Node.updated_at < since).all()
            node_ids = [item[1] for item in hosts]

            permanent_host_deletion.apply_async(queue='default_queue_ui_tasks', args=[node_ids])
        else:
            current_app.logger.info("Deleting limit not set, skipping ")
    except Exception as e:
        current_app.logger.error(e)
    current_app.logger.info("Task to purge older data is completed")


@celery.task()
def permanent_host_deletion(node_ids):
    if node_ids:
        current_app.logger.info("Hosts with ids {} are requested to delete permanently".format(node_ids))
        try:
            nodes = db.session.query(Node).filter(Node.id.in_(node_ids)).all()
            for node in nodes:
                node.tags = []
            db.session.commit()

            deleted_count = Node.query.filter(Node.state == Node.DELETED).filter(Node.id.in_(node_ids)).delete(synchronize_session=False)
            current_app.logger.info("{} hosts are deleted permanently".format(deleted_count))
        except Exception as e:
            current_app.logger.error("Unable to delete tags/result_log/status_log/alert_email/alerts from the node! " + str(e))
    else:
        current_app.logger.info("No host is requested to delete")
    db.session.commit()


def format_records(results):
    result_list = []
    keys = results.keys()

    data_list = results.fetchall()
    for data in data_list:
        result = {}
        for index, key in enumerate(keys):
            result[key] = data[index]
        result_list.append(result)
    return result_list


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        import decimal
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

