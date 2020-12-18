from vytals.utils import to_date, to_date_time, test_email_address
from datetime import datetime, date


def test_successful_to_date():
    valid_date = to_date("2001-11-14")

    assert isinstance(valid_date, date) is True
    assert valid_date


def test_successful_to_date_time():
    valid_datetime = to_date_time("2015-03-25T11:00:00")

    assert isinstance(valid_datetime, datetime) is True
    assert valid_datetime

