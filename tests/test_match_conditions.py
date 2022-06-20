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
def test_get_match_conditions(client):
    """
    Test create /user-input response for a valid user with authorization and
    valid input, ensure correct response.
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/match-conditions", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    full_res_str = '\n'.join([str(item) for item in full_res])

    resp.raise_for_status()
    matchdata_file = './tests/data/match_conditions_compare_dat.json'

    """ SERIALIZE STUDIES TO COMPARE AGAINST - UNCOMMENT TO WRITE NEW COMPARE DATA
    with open(matchdata_file,'w') as comp_file:
        json.dump(full_res, comp_file)
    """

    with open(matchdata_file, 'r') as comp_file:
        match_conditions_compare = json.load(comp_file)

    comp_study_id_list = [x['studyId'] for x in match_conditions_compare['body']]
    for study_comp in match_conditions_compare['body']:
        for study in full_res['body']:
            print(f"STUDY TYPE: {type(study)}")
            print(f"STUDY: {study}")
            # DOES THE STUDY IN THE RESPONSE EXIST IN THE SAVED DICT LIST? 
            if not study['studyId'] in comp_study_id_list:
                errors.append(f"STUDY: {study['studyId']} DOES NOT EXIT IN THE COMPARE FILE.")
            if study_comp['studyId'] == study['studyId']:
                diff = DeepDiff(study_comp, study)
                if diff:
                    errors.append(f"STUDY ID: {study_comp['studyId']} DOES NOT MATCH {diff}")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))            
