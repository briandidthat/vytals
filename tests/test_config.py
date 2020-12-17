import pytest

from vytals import init_app
from vytals.models import User, Role


@pytest.fixture(scope="module")
def new_user():
    user = User("snake", "test", "snakey", "123456", "snake@gmail.com", "2000-11-01")
    user.roles.append(Role("USER"))
    return user


@pytest.fixture(scope="module")
def test_client():
    app = init_app()
    app.config.from_object('config.DevelopmentConfig')

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
