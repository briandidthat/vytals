from vytals.utils import to_date
from datetime import datetime, date


def test_successful_to_date():
    valid_date = to_date("2001-11-14")

    assert isinstance(valid_date, date) is True
    assert valid_date
