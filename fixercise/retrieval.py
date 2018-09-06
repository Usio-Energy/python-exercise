# Principal script for getting and storing fixer rates data

import os.path
from datetime import datetime, timedelta
import logging

from fixercise.config import *
from fixercise.get_rates import *
from fixercise.storage import *


# Setup logging to log file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=os.path.join(LOG_DIR, "%s.log" % APP_NAME),
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('retrieval').addHandler(console)


def get_last_month_dates():
    """Returns a list of non_weekend dates in the past 31 days."""
    now = datetime.now()
    one_month_ago = now - timedelta(days=31)
    dates = []
    for d in range(0, 32):  # 32 because we want today as well
        active_date = one_month_ago + timedelta(days=d)
        if active_date.weekday() not in [5, 6]:
            dates.append(active_date)

    return [d.strftime("%Y-%m-%d") for d in dates]


def missing_month_dates():
    """Gets the dates missing from the past month.
        Takes the set difference between the dates that should exist
        for the past month and the dates that do exist in the data directory
    """
    historic_dates = list_historic_dates(DATA_DIR)

    return sorted(list(set(get_last_month_dates()) - set(historic_dates)))


def run():

    logging.info("Starting data retrieval")

    # Get a list of all dates to get
    dates_to_get = missing_month_dates()

    logging.info("%d dates to retrieve" % len(dates_to_get))

    for date in dates_to_get:
        print(date)
        try:
            logging.info("Getting rates for %s" % date)
            response = get_historic_rates(date)
            logging.info("Storing rates for %s" % date)
            store_rates(response, DATA_DIR)

        except BadResponseException as e:
            logging.error(e)

        except BadCallException as e:
            logging.error(e)

        except WeekendException:
            logging.warning("Tried to write data for weekend date %s" % date)
            continue

        logging.info("Looks like we're done.")







