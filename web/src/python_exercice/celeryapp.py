
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from raven import Client
from raven.contrib.celery import register_signal

from django.conf import settings

app = Celery('python_exercice')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf.settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if hasattr(settings, 'RAVEN_CONFIG'):
    # Celery signal registration
    client = Client(dsn=settings.RAVEN_CONFIG['dsn'])
    register_signal(client)