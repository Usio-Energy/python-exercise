import datetime
import os

from celery import Celery
from celery.schedules import crontab

from . import core

app = Celery('ingest', broker='redis://broker/1')
app.conf.timezone = 'Europe/London'


@app.on_after_configure.connect
def schedule(sender, **kwargs):
    'Set up scheduled tasks'
    sender.add_periodic_task(
        crontab(hour=9, minute=0, day_of_week='mon-fri'),
        run.s(),
        name='ingestion routine'
    )


@app.task
def run():
    'Download exchange rate data, store in database'
    data = core.get_data(datetime.date.today())
    _, table = core.connection_table()
    table.insert(data)
