"""
.. module:: python_exercice.config.common
   :synopsis: Common project settings, applies to all environments.
"""

from os.path import abspath, join, dirname

from django.utils.translation import ugettext_lazy as _
from celery.schedules import crontab

""" Paths """
PROJECT_ROOT = abspath(join(dirname(__file__), '..', '..'))
MEDIA_ROOT = join(PROJECT_ROOT, '..', '..', 'media')
STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'public'), ]
LOG_ROOT = join(PROJECT_ROOT, 'logs')

""" Urls """
STATIC_URL = '/s/'
MEDIA_URL = '/m/'
ROOT_URLCONF = 'python_exercice.urls'

""" Secret Key & Site ID """
SITE_ID = 1
SECRET_KEY = '4e+-29--0a=g9r(ihosdfo)jeqck6x@lf*6_#hqt_i-3(a9w_+s5'

""" Location """
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = (
    join(PROJECT_ROOT, 'locale/'),
)

""" Templates """
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(PROJECT_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Common django context processors
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

""" Middleware """
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

""" Installed Applications """
INSTALLED_APPS = (
    # Django Apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    # Third Party Apps here
    'django_extensions',
    # Project Apps here
    'python_exercice.currency',
)

""" Test Suite """
NOSE_ARGS = [
    '--include=^(can|it|ensure|must|should|specs?|examples?)',
    '--with-spec',
    '--spec-color',
    '-s',
]

""" Celery """
CELERYD_WORKER_LOST_WAIT = 30000
CELERY_TIMEZONE = 'Europe/London'

CELERYBEAT_SYNC_EVERY = 0

CELERYBEAT_SCHEDULE = {
    'store-currency-rate-database': {
        'task': 'store_currency_rate',
        'schedule': crontab(minute='0', hour='9', day_of_week='mon-fri'),
    },
}