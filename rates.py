#!/usr/bin/env python3

import logging
import sys
from contextlib import contextmanager
from datetime import date, timedelta
from pathlib import Path

import requests
from sqlalchemy import Column, Date, String, Float, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

DATABASE_LOCATION = Path(__file__).with_suffix('.sqlite')
API_KEY = 'a182bdf214377df85c8481ff9aaaa992'


@contextmanager
def db_session(db_file):
    """ Creates a context with an open SQLAlchemy session.
    """
    create_db = not db_file.exists()
    engine = create_engine(f'sqlite:///{db_file}', convert_unicode=True)
    if create_db:
        Base.metadata.create_all(engine)
    connection = engine.connect()
    session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    yield session
    session.close()
    connection.close()


class Rate(Base):
    __tablename__ = "rate"
    day = Column(Date, nullable=False, primary_key=True)
    currency = Column(String(3), primary_key=True)
    value = Column(Float)


def get_days(starting, ending=None, exclude_weekdays=()):
    one_day = timedelta(days=1)
    if ending is None:
        ending = date.today()
    while starting < ending:
        starting += one_day
        if starting.weekday() not in exclude_weekdays:
            yield starting


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    with db_session(DATABASE_LOCATION) as db:
        last_day = db.query(func.max(Rate.day).label('day')).one().day
        if last_day is None:
            start_day = date.today() - timedelta(days=30)
        else:
            start_day = last_day + timedelta(days=1)
        for day in get_days(start_day, exclude_weekdays=(5, 6)):
            response = requests.get(f'http://data.fixer.io/api/{day}?access_key={API_KEY}').json()
            logging.info(f'Reading exchange rates for {day}.')
            db.add_all(
                Rate(day=day, currency=currency, value=value) for currency, value in response['rates'].items()
            )
        db.commit()
