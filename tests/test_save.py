import pytest
import respx
from unittest.mock import patch
import json
from starlette.config import environ
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

@pytest.mark.parametrize(
    "data", [ 
        { 'data': [ {'value': 'TEST VALUE'} ], 'name': 'CREATE NAME 1' }
    ]
)
def test_create(setup_database, client, data):
    with patch('gearbox.routers.user_input.user_input_service.validate_user_input', return_value=None):
        """
        Test create /user-input response for a valid user with authorization and
        valid input, ensure correct response.
        """
        fake_jwt = "1.2.3"
        resp = client.post(
            "/user-input", json=data, headers={"Authorization": f"bearer {fake_jwt}"}
        )
        full_res = resp.json()
        resp.raise_for_status()

        assert str(resp.status_code).startswith("20")
        assert resp.json().get("id") is not None

@pytest.mark.parametrize(
    "data", [ 
        { 'data': [ {'id': 1, 'value': 'test response data for latest'} ], 'name': 'test last saved name' }
    ]
)
def test_get_last_saved_input(setup_database, client, data):
    """
    Test that the /user-input endpoint returns a 200 and the id of the latest saved obj
    """
    with patch('gearbox.routers.user_input.user_input_service.validate_user_input', return_value=None):
        errors = []
        fake_jwt = "1.2.3"
        resp = client.post(
            "/user-input", json=data, headers={"Authorization": f"bearer {fake_jwt}"}
        )
        resp = client.get("/user-input/latest", headers={"Authorization": f"bearer {fake_jwt}"})
        full_res = resp.json()

        if not resp.status_code == 200:
            errors.append(f"test_get_last_saved_input failed response code: {resp.status_code}")
        if not full_res['results'][0]['value'] == data['data'][0]['value']:
            errors.append(f"test_get_last_saved_input failed to retrieved last saved input: {data['data'][0]['value']}")

        assert not errors, "errors occurred: \n{}".format("\n".join(errors))

@pytest.mark.parametrize(
    "data", [ 
        { 'data': [ 
            {'id': 1, 'value': 'UPD: test response 1'},
            {'id': 2, 'value': 'UPD: test response 2'},
            {'id': 3, 'value': 'UPD: test response 3'} 
          ], 'id': 1, 'name': 'UPDATE SAVED NAME 1' }
    ]
)
def test_update_saved_input(setup_database, client, data):
    """
    Test that the /user-input endpoint returns a 200 and the id of the latest saved obj
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.post(
        "/user-input", json=data, headers={"Authorization": f"bearer {fake_jwt}"}
    )
    resp = client.get("/user-input/latest", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    if not resp.status_code == 200:
        errors.append(f"test_get_last_saved_input failed response code: {resp.status_code}")
    if not full_res['results'][0]['value'] == data['data'][0]['value']:
        errors.append(f"test_get_last_saved_input failed to retrieved last saved input: {data['data'][0]['value']}")
    
@pytest.mark.parametrize(
    "data", [ 
        { 'data': [ 
            {'id': 1, 'value': 'UPDATED: test response 1'},
            {'id': 2, 'value': 'UPDATED: test response 2'},
            {'id': 3, 'value': 'UPDATED: test response 3'} 
          ], 'id': 1 }
    ]
)

def test_get_all_saved_input(setup_database, client, data):
    """
    Test that the /user-input endpoint returns a 200 and all saved inputs for a user
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/user-input/all", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    if not resp.status_code == 200:
        errors.append(f"test_get_all_saved_input failed response code: {resp.status_code}")
    
    # check that the response contains the expected data (all of the saved inputs for the user)
    for saved_input in full_res:
        if not saved_input["results"] in data['data']:
            errors.append(f"test_get_all_saved_input failed to retrieved all saved inputs for user: {data['data']}")
