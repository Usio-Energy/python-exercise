from celery import Celery
from celery.schedules import crontab
from tasks import create_app
from tasks.tasks import process_rates, clean_rates


def create_celery(flask_application):
    """
    Creating the Celery application instance.
    :param obj flask_application: The Flask application instance.
    :return:
    """
    celery_app = Celery(flask_application.import_name,
                        broker=flask_application.config['BROKER_URL'])
    celery_app.conf.update(flask_application.config)
    celery_task = celery_app.Task

    class ContextTask(celery_task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_application.app_context():
                return celery_task.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


application = create_app(environment='development')
celery = create_celery(application)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Periodic task scheduler, the tasks referenced here will run at the specified time/frequency.
    :param obj sender: Sender instance to append new periodic tasks.
    :return:
    """
    sender.add_periodic_task(crontab(hour=9, minute=0, day_of_week='mon,tue,wed,thu,fri'),
                             process_rates, name='Process rates every morning 9.00 am during weekdays')
    sender.add_periodic_task(crontab(hour=9, minute=1, day_of_week='mon,tue,wed,thu,fri'),
                             clean_rates, name='Clean rates every morning 9.01 am during weekdays')
