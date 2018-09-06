import json
import os.path
from datetime import datetime


class WeekendException(Exception):
    """Custom exception for trying to write weekend data.
        In real life this logic wouldn't live here, but we were
         given a requirement to develop, and by jove, we
         are going to develop to that requirement
    """
    pass


def store_rates(rates, path):
    date = rates["date"]  # TODO: handle the keyerror exception somewhere

    # Check whether it's a weekend and throw exception if it's on the weekend
    rates_date = datetime.strptime(date, '%Y-%m-%d')

    if rates_date.weekday() not in range(0, 5):
        raise WeekendException

    filename = "%s_fixer_rates.json" % date
    filepath = os.path.join(path, filename)

    with open(filepath, "w") as f:
        f.write(json.dumps(rates))


def retrieve_rates(date, path):
    filename = "%s_fixer_rates.json" % date
    filepath = os.path.join(path, filename)

    with open(filepath, "r") as f:
        rates = json.load(f)

    return rates
