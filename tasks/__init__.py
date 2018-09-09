from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from dictalchemy import DictableModel
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from . import config

celery = Celery()
Base = declarative_base(cls=DictableModel)
db = SQLAlchemy()


def create_app(environment='development'):
    """Creates a Flask application"""
    config_map = {
        'development': config.Development(),
        'testing': config.Production(),
    }
    config_obj = config_map[environment.lower()]
    app = Flask(__name__)
    app.env = environment
    app.config.from_object(config_obj)
    celery.config_from_object(app.config)
    db.init_app(app)
    return app
