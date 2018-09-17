import pytest
import datetime

from ingest import bootstrap


@pytest.mark.parametrize('n,expected', [
     (3, ['2018-09-17']),
     (5, ['2018-09-17', '2018-09-14', '2018-09-13']),
     ]
)
def test_get_weekdays(n, expected):
    today = datetime.date(2018, 9, 17)
    assert list(map(str, bootstrap.get_weekdays(today, n=n))) == expected
