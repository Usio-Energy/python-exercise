import datetime

import sqlalchemy as sqla

from ingest import core


def main():
    'Bootstrap service with 30 days historical data'
    connection, table = core.connection_table()
    today = datetime.date.today()

    # the previous 30 weekdays
    dates_required = filter(
        lambda date: date.weekday() < 6,
        [today - datetime.timedelta(x) for x in range(30)]
    )

    # populate as needed
    for date in dates_required:
        exists = sqla.exists().where(table.c.date == date)
        if not connection.execute(sqla.select([exists])).scalar():
            table.insert(core.get_data(date)).execute()


if __name__ == '__main__':
    main()
