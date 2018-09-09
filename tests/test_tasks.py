from ..tasks.tasks import process_rates, clean_rates
from unittest.mock import Mock, call


def test_process_rates(monkeypatch):
    """
    Testing rates processing (succession of calls).
    :param monkeypatch: a monkeypatch instance.
    :return:
    """
    mocked_rates = Mock(json=Mock(return_value={'rates': {'EUR': '1'}}))
    mock = Mock(return_value=mocked_rates)
    monkeypatch.setattr('usio.tasks.tasks.fetch_rates', mock)
    monkeypatch.setattr('usio.tasks.tasks.prepare_rates', mock)
    monkeypatch.setattr('usio.tasks.tasks.store_rates', mock)
    process_rates()
    # First fetching the rates, then preparing the rates based on the json eventually storing the rates object.
    assert mock.mock_calls == [call(),
                               call({'EUR': '1'}),
                               call(mocked_rates)]
