import pytest
import json
import jwt

from httpx import AsyncClient
from fastapi import FastAPI

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

from gearbox import config

@respx.mock
@pytest.mark.parametrize(
    "data", [ 
        { 'data': [ {'id': 4, 'value': 'steve'} ] }
    ]
)
@pytest.mark.asyncio
def test_create(client, valid_upload_file_patcher, data):
    """
    Test create /user-input response for a valid user with authorization and
    valid input, ensure correct response.
    """
    print(f"DATA PARAMETER TYPE: {type(data)} ")
    print(f"DATA PARAMETER VALUE IN test_create: {data} ")
    fake_jwt = "1.2.3"
    resp = client.post(
        "/user-input", json=data, headers={"Authorization": f"bearer {fake_jwt}"}
    )
    print("HERE AFTER THE POST.. 1")
    full_res = resp.json()
    print(f"FULL RESPONSE: {full_res}")
    print(f"STATUS CODE: {resp.status_code}")

    resp.raise_for_status()
    print("HERE AFTER THE POST.. 2")

    res = resp.json().get("results")
    id = resp.json().get("id") 

    print(f"STATUS CODE: {resp.status_code}")
    print(f"RESULTS: {res}")
    print(f"ID: {id}")

    assert str(resp.status_code).startswith("20")
    assert resp.json().get("results") == data.get("data", {})
    assert resp.json().get("id") is not None

@respx.mock
def test_get_last_saved_input(client):
    """
    Test that the /user-input endpoint returns a 200 and the id of the latest saved obj
    """
    fake_jwt = "1.2.3"
    print("ABOUT TO CALL /user-input/latest")
    resp = client.get("/user-input/latest", headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == 200
    assert resp.json().get("id")  is not None 
