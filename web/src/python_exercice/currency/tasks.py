import requests
import json
from jsonschema import validate

from django.conf import settings

from python_exercice.celeryapp import app
from .models import CurrencyRate


FIXER_CURRENCY_JSON_SCHEMA = {
    'type': 'object',
    'properties': {
        'success': {
            'type': 'boolean',
            'const': True,
        },
        'date': {
            'type': 'string',
            'pattern': '^2[0-9]{3}-[0-1][0-9]-[0-3][0-9]$',
        },
        'base': {
            'type': 'string',
            'pattern': '^[A-Z]{3}$',
        },
        'rates': {
            'type': 'object',
            'patternProperties': {
                '^[A-Z]+$':  {
                    'type': 'number',
                }
            },
        },
    },
    'required': ['success', 'date', 'base', 'rates'],
}

@app.task(
    retry_backoff=True,
    max_retries=3,
    name='store_currency_rate'
)
def store_currency_rate(date='latest', api_mock_content=None):
    content = api_mock_content

    if not api_mock_content:
        request = requests.get(settings.FIXER_API_ENDPOINTS.format(date, settings.FIXER_API_ACCESS_KEY))

        if request.status_code != 200:
            raise Exception('Fixer Api call error, status: {}'.format(request.status_code))
            return False

        content = json.loads(request.content)

    # validate json format fixer api
    validate(content, FIXER_CURRENCY_JSON_SCHEMA)

    # store rate in db
    for currency, value in content['rates'].items():
        currency_rate, created = CurrencyRate.objects.get_or_create(
            currency_name = currency,
            currency_base_name = content['base'],
            date = content['date'],
            defaults={'rate': value},
        )

    return True
