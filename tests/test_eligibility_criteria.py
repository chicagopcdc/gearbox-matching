import pytest
import json

from deepdiff import DeepDiff

from httpx import AsyncClient
from fastapi import FastAPI

import tempfile
import respx

from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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

# auto_error=False prevents FastAPI from raises a 403 when the request is missing
# an Authorization header. Instead, we want to return a 401 to signify that we did
# not recieve valid credentials
bearer = HTTPBearer(auto_error=False)

# @pytest.mark.asyncio
def test_get_ec(client):
    """
    Test create /eligibility_criteria endpoint
    valid input, ensure correct response.
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/eligibility-criteria", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    full_res_str = '\n'.join([str(item) for item in full_res])

    resp.raise_for_status()
    ecdata_file = './tests/data/eligibilityCriteria.json'

    """ SERIALIZE STUDIES TO COMPARE AGAINST - UNCOMMENT TO WRITE NEW COMPARE DATA
    with open(ecdata_file,'w') as comp_file:
        json.dump(full_res, comp_file)
    """

    with open(ecdata_file, 'r') as comp_file:
        ec_compare = json.load(comp_file)

    diff = DeepDiff(full_res['body'], ec_compare, ignore_order=True)
    
    assert not diff, "differences occurred: \n{}".format("\n".join(diff))            
