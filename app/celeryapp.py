from celery import Celery
from celery.schedules import crontab
import os, inspect, json

def make_celery(app):
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    beat_schedule_map = os.path.join(currentDir, "celeryapp.json")
    with open(beat_schedule_map) as json_data:
        beat_schedule = json.load(json_data)
    celery.conf.beat_schedule = beat_schedule[app.config["CELERY_BEAT"]]
    return celery
