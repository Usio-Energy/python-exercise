import json
import os
from datetime import datetime


class WeekendException(Exception):
    """Custom exception for trying to write weekend data.
        In real life this logic wouldn't live here, but we were
         given a requirement to develop, and by jove, we
         are going to develop to that requirement
    """
    pass

# There are a lot of ways to persist data, but in this instance we are
# going with the time-honoured classic of writing it as a file to disk


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


def list_historic_dates(path):
    """Returns a list of dates we have historic rates for."""
    historic_rates = os.listdir(path)
    return [filename[:10] for filename in historic_rates]