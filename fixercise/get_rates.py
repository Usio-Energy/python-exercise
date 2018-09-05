import requests
import os

# For dev purposes, let's get this from an envvar
FIXER_API_KEY = os.getenv("FIXER_API_KEY", '')


def get_current_rates():
    # TODO: extract this URL somewhere
    response = requests.get(
        "http://data.fixer.io/api/latest?access_key=%s&format=1"
        % FIXER_API_KEY)

    # TODO: handle different status codes

    return response