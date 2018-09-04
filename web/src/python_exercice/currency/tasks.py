import requests
import json
from jsonschema import validate

from django.conf import settings

from python_exercice.celeryapp import app
from .models import CurrencyRate

# content = {
#   'success': True,
#   'timestamp':1536077348,
#   'base':'USD',
#   'date':'2018-09-04',
#   'rates':{
#     'AEA':4.248562,
#     'AFN':85.313513,
#     'ALL':126.454847,
#     'AMD':559.500481,
#   }
# }


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
def store_currency_rate():
    request = requests.get(settings.FIXER_API_ENDPOINTS)

    if request.status_code != 200:
        raise Exception('Fixer Api call error, status: {}'.format(request.status_code))
        return False
    else:
        content = json.loads(request.content)

        # validate json format fixer api
        validate(content, FIXER_CURRENCY_JSON_SCHEMA)

        for currency, value in content['rates'].items():
            currency_rate = CurrencyRate(
                currency_name = currency,
                currency_base_name = content['base'],
                date = content['date'],
                rate = value,
            )
            currency_rate.save()

    return True
