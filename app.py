from datetime import datetime
import json
from os import environ

import backoff
from psycopg2 import connect, OperationalError
import requests


api_key = environ.get('API_KEY')
request_string = f'http://data.fixer.io/api/latest?access_key={api_key}&format=1'


@backoff.on_exception(backoff.expo, OperationalError)
def get_cursor(*, host, port, user, password, db_name):
    """
    Get cursor for given parameters. If receives an operation error will wait
    and try again for DB to become operational (protects against disconnect).
    """
    conn = connect(
        host=host,
        port=port,
        dbname=db_name,
        user=user,
        password=password,
        connect_timeout=2
    )
    conn.set_session(autocommit=True)
    cursor = conn.cursor()

    return cursor


def main():
    json_data = requests.get(request_string).json()
    cursor = get_cursor(
        host='postgres_db',
        port=5432,
        user='postgres',
        password='postgrespass',
        db_name='currencies'
    )

    cursor.execute(
        'INSERT INTO daily_rates (day, rates) VALUES (%s, %s)',
        (datetime.utcnow(), json.dumps(json_data))
    )


if __name__ == '__main__':
    main()
