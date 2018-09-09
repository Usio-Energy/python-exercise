import requests
from uuid import uuid4
from .models import Rates
from .config import Config
from . import db


def fetch_rates():
    """
    Getting the rates from a third party API.
    n.b: warning, limit of 1000 calls/months for the free plan.
    :return:
    """
    rates_response = requests.get(Config.RATES_URL)
    if rates_response.status_code != 200:
        raise Exception('Warning, something went wrong during rates ingestion: {}'.format(rates_response.json()))
    return rates_response


def prepare_rates(rates_response):
    """
    Preparing the rates object to be stored.
    n.b: We store the rates directly in JSON format. It's a choice for more flexibility (drawback: data validation).
    :param dict rates_response: A json containing the rates data.
    :return obj rates: rates model object.
    """
    rates = Rates()
    rates.id = uuid4()
    rates.rates = rates_response
    return rates


def store_rates(rates):
    """
    Storing the rates data in the database.
    :param obj rates: Rates model object.
    :return:
    """
    db.session.add(rates)
    db.session.commit()
