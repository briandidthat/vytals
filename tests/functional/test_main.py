# TEST SUCCESSFUL Login and Registration attempts

def test_successful_login(test_client, init_database):
    response = test_client.post("/users/login", json={"username": "snakey", "password": "123456"})

    assert response.status_code == 200
    assert b"access_token" in response.data


def test_succesful_register(test_client, init_database):
    response = test_client.post("/users/new",
                                json=dict(firstName="testing", lastName="testings", username="shark", password="123456",
                                          email="shark@gmail.com", birthdate="2000-11-01"))

    assert response.status_code == 201
    assert b"access_token" in response.data


# ======================================================================================================================
#    TEST INVALID Login and Registration attempts

def test_register_with_duplicate(test_client, init_database):
    response = test_client.post("/users/new",
                                json=dict(firstName="snake", lastName="test", username="snakey", password="123456",
                                          email="snake@gmail.com", birthdate="2000-11-01"))

    assert response.status_code == 409
    assert b"That user already exists in the system." in response.data
    assert b"access_token" not in response.data


def test_login_with_invalid_credentials(test_client, init_database):
    response = test_client.post("/users/login",
                                json=dict(username="invalid", password="wrong"))

    assert response.status_code == 401
    assert b"Invalid login credentials." in response.data
    assert b"access_token" not in response.data
