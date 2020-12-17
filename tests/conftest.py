import pytest

from vytals import init_app, db
from vytals.models import Activity, User, Reading, Role


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
def test_client():
    app = init_app()
    app.config.from_object('config.DevelopmentConfig')

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database():
    db.create_all()

    user1 = User("snake", "test", "snakey", "123456", "snake@gmail.com", "2000-11-01")
    user2 = User("snake2", "test2", "snakey2", "123456", "snake2@gmail.com", "2000-11-04")
    role = Role("USER")

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(role)

    db.session.commit()

    yield db

    db.drop_all()
