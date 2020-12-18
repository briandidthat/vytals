from unittest.mock import patch
import json


# @patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
def test_create_activity(test_client, init_database):
    response = test_client.post("/activities/user/1/new",
                                json=dict(type="cleaning", description="cleaning the living room",
                                          startTime="2015-03-25T11:00:00", endTime="2015-03-25T11:39:00"))
    assert response.status_code == 201
    assert b"activity" in response.data


def test_get_activities(test_client, init_database):
    response = test_client.get("/activities/user/1/all")
    items = json.loads(response.data)

    assert response.status_code == 200
    assert b"activities" in response.data
    assert len(items["activities"]) == 1