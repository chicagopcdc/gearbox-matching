import pytest
import random
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
        {
            "code": "TESTCODE",
            "description": "string",
            "type": "string",
            "value_string": "string",
            "unit": "string",
            "operator": "string",
            "active": 1
    }
    ]
)
@pytest.mark.asyncio
def test_create_value(setup_database, client, valid_upload_file_patcher, data):
    """
    Test create value
    """
    fake_jwt = "1.2.3"
    data['code'] = 'PYTEST TESTCODE' + str(random.randint(0,9999))
    # add random value string to satisfy unique constraint for test
    data['value_string'] += data['code']
    resp = client.post("/value", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")

@pytest.mark.asyncio
def test_get_values(setup_database, client):
    """
    Test that the /values endpoint returns a 200 and the id of the latest saved obj
    """
    fake_jwt = "1.2.3"
    resp = client.get("/values", headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == 200

@pytest.mark.asyncio
def test_get_value(setup_database, client):
    """
    Test that the /values endpoint returns a 200 and the id of the latest saved obj
    """
    fake_jwt = "1.2.3"
    resp = client.get("/value/1", headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == 200


# TO DO: create test for violating unique constraint
