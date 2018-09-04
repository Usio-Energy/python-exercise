"""
.. module:: python_exercice.config.dev
   :synopsis: Development settings, all developers should use this which is
   designed to be used with the Docker Compose environment
"""

from os import environ
from sys import argv
from .common import *

ALLOWED_HOSTS = ['localhost']
BASE_URL = 'http://localhost'
TIME_ZONE = 'Europe/London'

# Ipython Notebook, bind to this ip so it can be forwarded
IPYTHON_ARGUMENTS = [
    '--ip=0.0.0.0',
]

""" Debugging (default True for development environment) """
DEBUG = True
ENVIRONMENT = 'dev'

""" Databases (default is mysql) """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': environ.get('MYSQL_DATABASE', 'python_exercice'),
        'USER': environ.get('MYSQL_USER', 'root'),
        'HOST': 'db',
        'PORT': 3306,
        'PASSWORD': environ.get('MYSQL_PASSWORD', 'root'),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

""" Caching (default is dummy, see django docs) """
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

""" Use MD5 Password Hashing for Dev - Speeds things up """
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_QUEUE = 0
REDIS_WEBSOCKET = 1

BROKER_URL = 'redis://redis/0'

CELERY_BROKER_URL = BROKER_URL

# FIXER.IO API
FIXER_API_ACCESS_KEY = '6601e795b9b564eb003fc11b77d4a720'
FIXER_API_ENDPOINTS = 'http://data.fixer.io/api/{}?access_key={}'
