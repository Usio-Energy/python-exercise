

class Config(object):
    """
    Base class for Config.
    """
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_TIMEZONE = 'Europe/Dublin'
    CELERY_SEND_TASK_SENT_EVENT = True
    RATES_URL = 'http://data.fixer.io/api/latest?access_key=58e89cb7202a71058260ffc2d152c020'


class Development(Config):
    """
    Development config for development environment.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://clement-daubrenet:postgres@localhost/usio'
    BROKER_URL = 'redis://guest@localhost:6379/'


class Production(Config):
    """
    Production config for production environment.
    """
    SQLALCHEMY_DATABASE_URI = 'PRODUCTION-DATABASE'
    BROKER_URL = 'PRODUCTION-BROKER'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'output': {
                'format': '%(levelname)s %(asctime)s %(module)s Line: %(lineno)d Message: %(message)s',
            }
        },
        'handlers': {
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'output',
                'filename': '/var/log/web_apps/prod_usio.log',
                'backupCount': 5,
                'maxBytes': 1048576,
                'encoding': 'utf-8'
            },
            'smtp': {
                'class': 'logging.handlers.SMTPHandler',
                'level': 'ERROR',
                'formatter': 'output',
                'mailhost': 'localhost',
                'toaddrs': ['notifications@test.com'],
                'subject': '[USIO - PROD] Error encountered.',
            },
        },
        'loggers': {
            'flask-io': {
                'handlers': ['file', 'smtp'],
                'level': 'ERROR'
            },
            'webapi': {
                'handlers': ['file', 'smtp'],
                'level': 'INFO'
            }
        }
    }
