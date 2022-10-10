import pytest

import json

from deepdiff import DeepDiff

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
    resp = client.get("/build-studies", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    resp.raise_for_status()

    assert str(resp.status_code).startswith("20")
    
# @pytest.mark.asyncio
def test_get_studies_compare(setup_database, client):
    """
    Test get /studies endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/build-studies", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    full_res_str = '\n'.join([str(item) for item in full_res])

    resp.raise_for_status()
    studydata_file = './tests/data/studies.json'

    """ SERIALIZE STUDIES TO COMPARE AGAINST - UNCOMMENT TO WRITE NEW COMPARE DATA
    with open(studydata_file,'w') as comp_file:
        json.dump(full_res, comp_file)
    """

    with open(studydata_file, 'r') as comp_file:
        study_compare = json.load(comp_file)

    diff = []
    # Diff all studies in the reponse that exist in the mock file
    for i in range (len(study_compare)):
        study_diff = DeepDiff(full_res[i], study_compare[i], ignore_order=True)
        if (study_diff):
            diff.append(study_diff)
    
    assert not diff, "differences occurred: \n{}".format("\n".join(diff))            
