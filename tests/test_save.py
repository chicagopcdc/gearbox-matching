import pytest

import httpx
import respx
from fastapi import HTTPException
from starlette.config import environ
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from mds import config


def test_create_no_auth_header(client, valid_upload_file_patcher):
    """
    Test that no token results in 401
    """
    valid_upload_file_patcher["access_token_mock"].side_effect = Exception(
        "token not defined"
    )
    data = {
        "data": [{"id": 4, "value": "luca"}]
    }

    resp = client.post("/save", json=data)
    assert str(resp.status_code) == "401"



def test_create_invalid_token(client, valid_upload_file_patcher):
    """
    Test that a bad token results in 401
    """
    fake_jwt = "1.2.3"
    valid_upload_file_patcher["access_token_mock"].side_effect = HTTPException(
        HTTP_403_FORBIDDEN, "bad token"
    )
    data = {
        "data": [{"id": 4, "value": "luca"}]
    }

    resp = client.post(
        "/save", json=data, headers={"Authorization": f"bearer {fake_jwt}"}
    )
    assert str(resp.status_code) == "401"



@respx.mock
@pytest.mark.parametrize(
    "data",
    {
        "data": [{"id": 4, "value": "luca"}]
    },
)
def test_create(client, valid_upload_file_patcher, data):
    """
    Test create /save response for a valid user with authorization and
    valid input, ensure correct response.
    """
    fake_jwt = "1.2.3"
    resp = client.post(
        "/save", json=data, headers={"Authorization": f"bearer {fake_jwt}"}
    )
    resp.raise_for_status()

    assert str(resp.status_code).startswith("20")
    assert resp.json().get("results") == data.get("data", {})
    assert resp.json().get("id") is not None
    

@respx.mock
@pytest.mark.parametrize(
    "data",
    {
        "data": [{"id": 4, "value": "matteo"}],
        "id": 1
    },
)
def test_update(client, valid_upload_file_patcher, data):
    """
    Test update /save response for a valid user with authorization and
    valid input, ensure correct response.
    """
    fake_jwt = "1.2.3"
    resp = client.post(
        "/save", json=data, headers={"Authorization": f"bearer {fake_jwt}"}
    )
    resp.raise_for_status()

    assert str(resp.status_code).startswith("20")
    assert resp.json().get("results") == data.get("data", {})
    assert resp.json().get("id") == data.get("id")



@respx.mock
def test_get_last_saved_input(client):
    """
    Test that the /save endpoint returns a 200 and the id of the latest saved obj
    """
    fake_jwt = "1.2.3"
    resp = client.get("/save/latest", headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == 200
    assert resp.json().get("id")  is not None 





