from datetime import date, datetime


def test_new_user_with_fixture(new_user):
    assert new_user.first_name == "snake"
    assert new_user.last_name == "test"
    assert new_user.username == "snakey"
    assert new_user.password != "123456"
    assert new_user.email == "snake@gmail.com"
    assert new_user.birthdate == date.fromisoformat("2000-11-01")


def test_new_activity(new_activity):
    assert new_activity.type == "Cooking"
    assert new_activity.description == "Cooking chicken soup at home"
    assert new_activity.start_time == datetime.fromisoformat("2015-03-25T12:00:00")
    assert new_activity.end_time == datetime.fromisoformat("2015-03-25T12:39:00")
    assert new_activity.user_id == 1


def test_new_reading_with_fixture(new_reading):
    assert new_reading.weight == 115.3
    assert new_reading.blood_pressure == 111
    assert new_reading.temperature == 97.9
    assert new_reading.oxygen_level == 97
    assert new_reading.pulse == 89
    assert new_reading.timestamp == datetime.fromisoformat("2015-04-25T12:00:00")
    assert new_reading.user_id == 1
