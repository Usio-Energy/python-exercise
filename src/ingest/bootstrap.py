import datetime

import sqlalchemy as sqla

from ingest import core


def get_weekdays(today, n=30):
    'Return a list of the weekdays in the n previous days from today'
    return filter(
        lambda date: date.weekday() < 5,
        [today - datetime.timedelta(x) for x in range(n)]
    )


def main():
    'Bootstrap service with 30 days historical data'
    connection, table = core.connection_table()
    for date in get_weekdays(datetime.date.today()):
        exists = sqla.exists().where(table.c.date == date)
        if not connection.execute(sqla.select([exists])).scalar():
            table.insert(core.get_data(date)).execute()


if __name__ == '__main__':
    main()
