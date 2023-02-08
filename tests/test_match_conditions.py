import pytest
import json
import jwt
import random

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
@pytest.mark.asyncio
def test_build_mc(setup_database, client, valid_upload_file_patcher):
    """
    Test create value
    """
    fake_jwt = "1.2.3"
    # add random value string to satisfy unique constraint for test
    resp = client.post("/build-match-conditions", headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    full_res = resp.json()
    assert str(resp.status_code).startswith("20")
