class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/0'
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Development.db'
    CELERY_BEAT = "DEVELOPMENT"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Testing.db'
    CELERY_BEAT = "DEVELOPMENT"

class ProductionConfig(Config):
    DEBUG = False    
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Production.db'
    CELERY_BEAT = "PRODUCTION"

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
