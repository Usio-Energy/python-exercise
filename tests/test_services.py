from ..tasks.services import prepare_rates, fetch_rates
from unittest.mock import Mock
from uuid import UUID
import pytest


def test_fetch_rates_ok(monkeypatch):
    """
    Testing the rates fetching: valid scenario with 200 response http code.
    :param monkeypatch: A monkeypatch instance.
    :return:
    """
    response_mock = Mock(return_value=Mock(status_code=200, json=Mock(return_value={'rates': 'OK'})))
    monkeypatch.setattr('usio.tasks.services.requests.get', response_mock)
    response_rates = fetch_rates()
    assert response_mock.call_count == 1
    assert response_rates.json() == {'rates': 'OK'}


def test_fetch_rates_nok(monkeypatch):
    """
    Testing the rates fetching: error scenario with 500 http code.
    :param monkeypatch: A monkeypatch instance.
    :return:
    """
    response_mock = Mock(return_value=Mock(status_code=500, json=Mock(return_value={'error': 'internal error'})))
    monkeypatch.setattr('usio.tasks.services.requests.get', response_mock)
    with pytest.raises(Exception,
                       message="Warning, something went wrong during rates ingestion: {'error': 'internal error'}"):
        fetch_rates()


def test_prepare_rates():
    """
    Testing the rates preparation: checking that the fields are correctly set.
    :return:
    """
    rates_response = {"success": True, "timestamp": 1536410652, "base": "EUR", "date": "2018-09-08",
                      "rates": {"AED": 4.250573, "AFN": 85.66226, "ALL": 126.597086, "AMD": 560.860654,
                                "ANG": 2.136972, "AOA": 327.371721, "ARS": 42.854029, "AUD": 1.627771,
                                "AWG": 2.074196, "AZN": 1.970057, "BAM": 1.844621, "BBD": 2.318644,
                                "BDT": 97.090918, "BGN": 1.958832, "BHD": 0.436241, "BIF": 2050.474019, "BMD": 1.157152,
                                "BND": 1.748377}}
    rates = prepare_rates(rates_response)
    assert type(rates.id) is UUID
    assert rates.rates == rates_response
