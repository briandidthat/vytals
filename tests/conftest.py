import pytest

from vytals import init_app, db
from vytals.models import Activity, User, Reading, Role
from flask_jwt_extended import create_access_token


@pytest.fixture(scope="module")
def new_user():
    user = User("snake", "test", "snakey", "123456", "snake@gmail.com", "2000-11-01")
    user.id = 1
    return user


@pytest.fixture(scope="module")
def new_activity():
    activity = Activity("Cooking", "Cooking chicken soup at home", "2015-03-25T12:00:00", "2015-03-25T12:39:00", 1)
    return activity


@pytest.fixture(scope="module")
def new_reading():
    reading = Reading(115.3, 111, 97.9, 97, 89, "2015-04-25T12:00:00", 1)
    return reading


@pytest.fixture(scope="module")
def access_token():
    user = User("snake", "test", "snakey", "123456", "snake@gmail.com", "2000-11-01")
    user.roles.append(Role("USER"))
    token = create_access_token(identity=user)
    return token


@pytest.fixture(scope="module")
def test_client():
    app = init_app()
    app.config.from_object('config.DevelopmentConfig')

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="function")
def init_database():
    db.create_all()

    user = User("snake", "test", "snakey", "123456", "snake@gmail.com", "2000-11-01")
    role = Role("USER")
    activity = Activity("Cooking", "Cooking chicken soup at home", "2015-03-25T12:00:00", "2015-03-25T12:39:00", 1)
    reading = Reading(115.3, 111, 97.9, 97, 89, "2015-04-25T12:00:00", 1)

    db.session.add(user)
    db.session.add(role)
    db.session.add(activity)
    db.session.add(reading)
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()
