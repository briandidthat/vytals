import json

# TEST SUCCESSFUL Reading requests


def test_successful_create_reading(test_client, init_database):
    response = test_client.post("/readings/user/1/new",
                                json=dict(weight=115.3, bloodPressure=111, temperature=97.9, oxygenLevel=97,
                                          pulse=89, timestamp="2015-04-25T12:00:00"))

    assert response.status_code == 201
    assert b"reading" in response.data


def test_successful_get_readings(test_client, init_database):
    response = test_client.get("/readings/user/1/all")
    items = json.loads(response.data)

    assert response.status_code == 200
    assert b"readings" in response.data
    assert len(items['readings']) == 1


# ======================================================================================================================
# TEST INVALID Reading requests

def test_create_reading_with_invalid_user(test_client, init_database):
    response = test_client.post("/readings/user/123/new",
                                json=dict(weight=115.3, bloodPressure=111, temperature=97.9, oxygenLevel=97,
                                          pulse=89, timestamp="2015-04-25T12:00:00"))

    assert response.status_code == 404
    assert b"There is no user associated with the id provided." in response.data


def test_create_reading_with_invalid_timestamp(test_client, init_database):
    response = test_client.post("/readings/user/1/new",
                                json=dict(weight=115.3, bloodPressure=111, temperature=97.9, oxygenLevel=97,
                                          pulse=89, timestamp="2015-04-25T12:asdd"))

    assert response.status_code == 422
    assert b"reading" not in response.data
    assert b"must be of datetime type" in response.data


def test_get_readings_with_invalid_user(test_client, init_database):
    response = test_client.get("/readings/user/123/all")

    assert response.status_code == 404
    assert b"There are no readings associated with the id provided." in response.data
