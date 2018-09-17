import os

import requests
import sqlalchemy as sqla


def get_data(date):
    'Get exchange rates for a particular date using Fixer API'
    response = requests.get(
        "http://data.fixer.io/api/{0}?access_key={1}".format(
            date,
            os.environ['FIXER_API_KEY'],
        )
    )
    data = response.json()
    data.pop('historical')  # this is meaningless here
    assert data['success']  # avoid db explosion
    return data


def connection_table():
    'Return a tuple of database connection and response table'
    engine = sqla.create_engine('postgresql+pg8000://postgres:@storage/ingest')
    connection = engine.connect()
    meta = sqla.MetaData(bind=connection)

    # a bit lazy, uses
    # http://docs.sqlalchemy.org/en/latest/core/reflection.html
    table = sqla.Table('response', meta, autoload=True)

    return connection, table
