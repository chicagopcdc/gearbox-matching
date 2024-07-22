import pytest
import respx
from fastapi import HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from os import environ

# input_data = {
#     #input_type: criterion id with that type
#     'num_Integer': 10, 
#     'radio_list': 3, 
#     'num_percentage': 17, 
#     'num_Float': 2, 
#     'select_list': 8, 
#     'age_integer': 1, 
# }

@pytest.fixture(scope='module')
def send_validation_request_function(client):
    # og_dummy_user = environ.get("BYPASS_FENCE_DUMMYER_USER_ID")
    # environ["BYPASS_FENCE_DUMMYER_USER_ID"] = str(int(og_dummy_user) + 1)
    def send_validation_request(data):
        fake_jwt = "1.2.3"
        resp = client.post(
            "/user-input", json=data, headers={"Authorization": f"bearer {fake_jwt}"}
        )
        return (resp.status_code, resp.json())

    yield send_validation_request

    # environ["BYPASS_FENCE_DUMMYER_USER_ID"] = og_dummy_user

@pytest.fixture(scope='module')
def id(client):
    fake_jwt = "1.2.3"
    resp = client.get("/user-input/latest", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    yield full_res["id"]

@pytest.mark.run(order=1)
def test_admin_load_data(client):
    """
    Test get /user-input/validation-update response for a valid admin with authorization, 
    ensure correct response.
    """
    fake_jwt = "1.2.3"
    resp = client.get(
        "/user-input/validation-update",  headers={"Authorization": f"bearer {fake_jwt}"}
    )
    resp.raise_for_status()

    assert str(resp.status_code).startswith("20")
    assert resp.json() == "user_validation data cleared"

@pytest.mark.run(order=2)
def test_send_first_input_request(send_validation_request_function):

    status_code, json_data = send_validation_request_function({"data": [{"id": 1, "value": "2"}]})
    assert status_code == 200


def test_invalid_format(send_validation_request_function):
    status_code, json_data = send_validation_request_function({"data": [{"value": "2"}]})
    assert status_code == 400
    assert json_data['detail'] == "incorrect format in input: {'value': '2'}."

    status_code, json_data = send_validation_request_function({"data": [{"id": 2}]})
    assert status_code == 400
    assert json_data['detail'] == "incorrect format in input: {'id': 2}."

    status_code, json_data = send_validation_request_function({"data": [{"id": "2"}]})
    assert status_code == 400
    assert json_data['detail'] == "incorrect format in input: {'id': '2'}."
    
    status_code, json_data = send_validation_request_function({"data": [{"id": "2", "value": []}]})
    assert status_code == 400
    assert json_data['detail'] == "incorrect format in input: {'id': '2', 'value': []}."

def test_number_Integer(send_validation_request_function, id):
    #test correct
    status_code, json_data = send_validation_request_function({"data": [{"id": 10, "value": "2"}], "id": id})
    assert status_code == 200
    
    message = 'must be a string containing an integer'
    status_code, json_data = send_validation_request_function({"data": [{"id": 10, "value": 2}], "id": 1})
    assert status_code == 400
    assert message in json_data['detail']

    status_code, json_data = send_validation_request_function({"data": [{"id": 10, "value": "2.7"}], "id": 1})
    assert status_code == 400
    assert message in json_data['detail']

def test_age_integer(send_validation_request_function, id):
    #test correct
    print(id)
    status_code, json_data = send_validation_request_function({"data": [{"id": 1, "value": "2"}], "id": id})
    assert status_code == 200
    
    message = 'must be a string containing an integer'
    status_code, json_data = send_validation_request_function({"data": [{"id": 1, "value": 2}]})
    assert status_code == 400
    assert message in json_data['detail']

    status_code, json_data = send_validation_request_function({"data": [{"id": 1, "value": "2.7"}]})
    assert status_code == 400
    assert message in json_data['detail']

def test_num_float(send_validation_request_function, id):
    #test correct
    status_code, json_data = send_validation_request_function({"data": [{"id": 2, "value": "2.2"}], "id": id})
    assert status_code == 200

    status_code, json_data = send_validation_request_function({"data": [{"id": 2, "value": "2"}], "id": id})
    assert status_code == 200

    message = 'must be a string containing a floating point number'
    status_code, json_data = send_validation_request_function({"data": [{"id": 2, "value": 2}], "id": 4})
    assert status_code == 400
    print(json_data['detail'])
    assert message in json_data['detail']

    status_code, json_data = send_validation_request_function({"data": [{"id": 2, "value": "ehllo"}], "id": 4})
    assert status_code == 400
    assert message in json_data['detail']

def test_percentage_float(send_validation_request_function, id):
    #test correct
    status_code, json_data = send_validation_request_function({"data": [{"id": 17, "value": "2.2"}], "id": id})
    assert status_code == 200

    status_code, json_data = send_validation_request_function({"data": [{"id": 17, "value": "2"}], "id": id})
    assert status_code == 200

    message = 'must be a string containing a floating point number'
    status_code, json_data = send_validation_request_function({"data": [{"id": 17, "value": 2}], "id": 4})
    assert status_code == 400
    print(json_data['detail'])
    assert message in json_data['detail']

    status_code, json_data = send_validation_request_function({"data": [{"id": 17, "value": "ehllo"}], "id": 4})
    assert status_code == 400
    assert message in json_data['detail']

def test_radio_list(send_validation_request_function, id):
    #test correct
    status_code, json_data = send_validation_request_function({"data": [{"id": 3, "value": 1}], "id": id})
    assert status_code == 200

    status_code, json_data = send_validation_request_function({"data": [{"id": 3, "value": 2}], "id": id})
    assert status_code == 200

    message = 'must be an integer'
    status_code, json_data = send_validation_request_function({"data": [{"id": 3, "value": "2"}], "id": 4})
    assert status_code == 400
    print(json_data['detail'])
    assert message in json_data['detail']

    message = 'is not one of the valid options'
    status_code, json_data = send_validation_request_function({"data": [{"id": 3, "value": 4}], "id": 4})
    assert status_code == 400
    print(json_data['detail'])
    assert message in json_data['detail']


def test_select_list(send_validation_request_function, id):
    #test correct
    status_code, json_data = send_validation_request_function({"data": [{"id": 8, "value": 7}], "id": id})
    assert status_code == 200

    status_code, json_data = send_validation_request_function({"data": [{"id": 8, "value": 6}], "id": id})
    assert status_code == 200

    message = 'must be an integer'
    status_code, json_data = send_validation_request_function({"data": [{"id": 8, "value": "2"}], "id": 4})
    assert status_code == 400
    print(json_data['detail'])
    assert message in json_data['detail']

    message = 'is not one of the valid options'
    status_code, json_data = send_validation_request_function({"data": [{"id": 8, "value": 4}], "id": 4})
    assert status_code == 400
    print(json_data['detail'])
    assert message in json_data['detail']

def test_multi(send_validation_request_function, id):
    status_code, json_data = send_validation_request_function({"data": [{"id": 8, "value": 7}, {"id": 2, "value": "2.2"}], "id": id})
    assert status_code == 200

    message = 'is not one of the valid options'
    status_code, json_data = send_validation_request_function({"data": [{"id": 2, "value": "2.2"}, {"id": 8, "value": 4}], "id": 4})
    assert status_code == 400
    print(json_data['detail'])
    assert message in json_data['detail']