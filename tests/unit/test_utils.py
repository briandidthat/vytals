from vytals.utils import to_date, to_date_time, test_email_address as email_validator
from datetime import datetime, date


def test_successful_to_date():
    valid_date = to_date("2001-11-14")

    assert valid_date
    assert isinstance(valid_date, date) is True
    assert valid_date.month == 11
    assert valid_date.day == 14
    assert valid_date.year == 2001


def test_successful_to_date_time():
    valid_datetime = to_date_time("2015-03-25T11:00:00")

    assert valid_datetime
    assert isinstance(valid_datetime, datetime) is True
    assert valid_datetime.day == 25
    assert valid_datetime.hour == 11
    assert valid_datetime.month == 3
    assert valid_datetime.year == 2015


def test_successful_email_address_input():
    valid_email = email_validator("test@gmail.com")

    assert valid_email
    assert isinstance(valid_email, str)


def test_to_date_with_invalid_date():
    invalid_date = to_date("2222-11-51")

    assert invalid_date is False
