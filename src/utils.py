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


class SessionManager:
    def __init__(self, autocommit=False):
        self.session = None
        self._autocommit = autocommit

    def __enter__(self):
        self.session = create_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.session.rollback()
        if self._autocommit is True:
            self.session.commit()
