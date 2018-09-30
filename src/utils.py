import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.sql.expression import ClauseElement


def create_default_engine():
    database_url = os.environ['DATABASE_URL']
    return create_engine(database_url, echo=False)


def create_session(engine=None):
    if engine is None:
        engine = create_default_engine()
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()
