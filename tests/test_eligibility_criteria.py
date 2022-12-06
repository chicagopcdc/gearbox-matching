import pytest
import json
from .test_utils import is_aws_url

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
def test_build_ec(setup_database, client):
    """
    Test create /eligibility_criteria endpoint
    valid input, ensure correct response.
    """
    
    fake_jwt = "1.2.3"
    resp = client.post("/build-eligibility-criteria", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    resp.raise_for_status()
    ecdata_file = './tests/data/eligibilityCriteria.json'

    """ SERIALIZE STUDIES TO COMPARE AGAINST - UNCOMMENT TO WRITE NEW COMPARE DATA
    with open(ecdata_file,'w') as comp_file:
        json.dump(full_res, comp_file)
    """

    with open(ecdata_file, 'r') as comp_file:
        ec_compare = json.load(comp_file)

    diff = []
    for i in range (len(ec_compare)):
        ec_diff = DeepDiff(full_res[i], ec_compare[i], ignore_order=True)
        if ec_diff:
            diff.append(ec_diff)
    
    assert not diff, "differences occurred: \n{}".format("\n".join(diff))            

def test_get_ec(setup_database, client):
    errors = []
    fake_jwt = "1.2.3"
    url = client.get("/eligibility-criteria", headers={"Authorization": f"bearer {fake_jwt}"})
    url_str =  url.content.decode('ascii').strip('\"')

    assert is_aws_url(url_str)
