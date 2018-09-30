import unittest

from exceptions import InvalidResponseCodeException
from models import Batch, Currency, CurrencyRate
from tests.utils import TempSQLliteTestCase

from unittest.mock import patch

from main import (get_fixer_data,
                  get_or_create_currency_instances,
                  save_batch,
                  save_rates)


class TestGetOrCreateCurrencyInstances(TempSQLliteTestCase):
    def test_get_or_create(self):
        session = self.create_session()
        already_existing_currency = 'GBP'
        currency_to_create = 'EUR'
        session.add(Currency(code=already_existing_currency))
        session.transaction.commit()
        self.assertEqual(session.query(Currency).count(), 1)
        currencies = get_or_create_currency_instances(
            [already_existing_currency, currency_to_create], session=session)
        self.assertSetEqual({currency_to_create, already_existing_currency},
                            {currency.code for currency in currencies})
        self.assertEqual(session.query(Currency).count(), 2)


class TestSaveBatch(unittest.TestCase):
    def test_save_batch(self):
        date_str = '2018-05-8'
        base_currency = Currency(code='GBP')
        batch = save_batch(date_str=date_str,
                           base_currency=base_currency,
                           session=DummySession())
        self.assertIsInstance(batch, Batch)


class TestSaveRate(unittest.TestCase):
    def test_save_rates(self):
        batch = Batch()
        rates_dict = {'USD': 5, 'GBP': 6}
        currency_code_inst_dict = {code: Currency(code=code)
                                   for code in rates_dict.keys()}
        rates = save_rates(rates_dict, batch,
                           currency_code_inst_dict, DummySession())
        for rate in rates:
            self.assertIsInstance(rate, CurrencyRate)


class TestGetFixerdata(unittest.TestCase):
    def test_get_fixer_data_raises_exception(self):
        dummy_response = DummyResponse(False, 404, {'success': False})
        with patch(target='main.requests.get',
                   return_value=dummy_response) as p:
            with self.assertRaises(InvalidResponseCodeException):
                get_fixer_data(None, None, None)

    def test_get_data_no_exception(self):
        dummy_response = DummyResponse(True, 200, {'success': True})
        with patch(target='main.requests.get',
                   return_value=dummy_response) as p:
            get_fixer_data(None, None, None)


# Utils to help with testing


class DummyResponse:
    def __init__(self, ok, status_code, data):
        self.ok = ok
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data


class DummySession:
    def add(self, item):
        pass

    def add_all(self, items):
        pass