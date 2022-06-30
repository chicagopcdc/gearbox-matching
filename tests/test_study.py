import pytest

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

# @pytest.mark.asyncio
def test_get_studies(setup_database, client):
    """
    Test create /user-input response for a valid user with authorization and
    valid input, ensure correct response.
    """
    fake_jwt = "1.2.3"
    resp = client.get("/studies", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    resp.raise_for_status()

    print(f"STATUS CODE: {resp.status_code}")
    assert str(resp.status_code).startswith("20")
    
