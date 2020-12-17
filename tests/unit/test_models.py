from datetime import date, datetime

from vytals.models import User


def test_new_user():
    user = User("snake", "test", "snakey", "123456", "snake@gmail.com", "2000-11-01")

    assert user.first_name == "snake"
    assert user.last_name == "test"
    assert user.username == "snakey"
    assert user.password != "123456"
    assert user.email == "snake@gmail.com"
    assert user.birthdate == date.fromisoformat("2000-11-01")
