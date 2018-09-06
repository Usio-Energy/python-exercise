import requests

from fixercise.config import *


# Let's define ourselves some new exceptions
class BadResponseException(Exception):
    """We raise this when we don't get a 200 response."""
    pass


class BadCallException(Exception):
    """We raise this when we get a failed API call."""
    pass


def get_current_rates():
    response = requests.get(
        "%s/latest?access_key=%s&format=1"
        % (FIXER_API_URL, FIXER_API_KEY))

    if response.status_code != 200:
        raise BadResponseException("Response returned status %d"
                                   % response.status_code)

    data = response.json()

    if not data["success"]:
        raise BadCallException(data["error"])

    return data


def get_historic_rates(historic_date):
    """Gets rates from a historic date.
        historic_date is ISO date-formatted string YYYY-MM-DD
    """
    response = requests.get(
        "%s/%s?access_key=%s&format=1"
        % (FIXER_API_URL, historic_date, FIXER_API_KEY))

    if response.status_code != 200:
        raise BadResponseException("Response returned status %d"
                                   % response.status_code)

    data = response.json()
    if not data["success"]:
        raise BadCallException(data["error"])

    return data
