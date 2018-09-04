from __future__ import absolute_import, unicode_literals
import sys

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
try:
    from .celeryapp import app as celery_app
    __all__ = ['celery_app']
except ImportError:
    sys.stdout.write('Celery not found')

__VERSION__ = '1.1.0'
