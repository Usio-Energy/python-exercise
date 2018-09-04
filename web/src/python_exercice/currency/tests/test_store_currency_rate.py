import datetime

from jsonschema.exceptions import ValidationError

from django.test import TestCase, override_settings

from python_exercice.currency.models import *
from python_exercice.currency.tasks import store_currency_rate


INVALID_MOCK_CONTENT_UNSUCCESSED = {
    'success': False,
    'timestamp': 1536077348,
    'base':'EUR',
    'date':'2018-09-04',
    'rates': {
        'AFN': 85.313513,
        'ALL': 126.454847,
        'AMD': 559.500481,
    }
}

INVALID_MOCK_CONTENT_MISSING_DATE = {
    'success': False,
    'timestamp': 1536077348,
    'base':'EUR',
    'date':'2018-09-04',
    'rates': {
        'AFN': 85.313513,
        'ALL': 126.454847,
        'AMD': 559.500481,
    }
}

class StoreCurrencyRateTests(TestCase):

    def test_fixer_unsuccessful(self):
        self.assertRaises(ValidationError, store_currency_rate, INVALID_MOCK_CONTENT_UNSUCCESSED)
    
    def test_fixer_missing_date(self):
        self.assertRaises(ValidationError, store_currency_rate, INVALID_MOCK_CONTENT_MISSING_DATE)

    @override_settings(FIXER_API_ENDPOINTS='http://data.fixer.io/api/latest?access_key=0')
    def test_fixer_wrong_endpoint_key(self):
        self.assertRaises(ValidationError, store_currency_rate)

    def test_fixer_store_rate_successfully(self):
        store_currency_rate()
        self.assertTrue(CurrencyRate.objects.count() >=1)
        first_currency_rate = CurrencyRate.objects.first()
        self.assertTrue(type(first_currency_rate.currency_name), str)
        self.assertTrue(type(first_currency_rate.currency_base_name) == str)
        self.assertTrue(type(first_currency_rate.rate) == float and first_currency_rate.rate > 0)
        self.assertTrue(type(first_currency_rate.date) == datetime.date)
        
        # test unique rate per date/base/currency
        store_currency_rate()
        count_duplicate_first_item = CurrencyRate.objects.filter(
            currency_name=first_currency_rate.currency_name,
            currency_base_name=first_currency_rate.currency_base_name,
            date=first_currency_rate.date,
        ).count()
        self.assertTrue(count_duplicate_first_item == 1)