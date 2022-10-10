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
def test_get_match_form(setup_database, client):
    """
    Test create /match_form endpoint
    valid input, ensure correct response.
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/match-form", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    resp.raise_for_status()
    matchformdata_file = './tests/data/match_form_compare_dat.json'

    """ SERIALIZE STUDIES TO COMPARE AGAINST - UNCOMMENT TO WRITE NEW COMPARE DATA
        MANUALLY VALIDATE MATCH FORM BEFORE UNCOMMENTING 
    with open(matchformdata_file,'w') as comp_file:
        json.dump(full_res, comp_file)
    """

    with open(matchformdata_file, 'r') as comp_file:
        match_form_compare = json.load(comp_file)
    
    comp_group_id_list = [x['id'] for x in match_form_compare['groups']]
    comp_field_id_list = [x['id'] for x in match_form_compare['fields']]

    for group_comp in match_form_compare['groups']:
        for group in full_res['groups']:
            if not group['id'] in comp_group_id_list:
                errors.append(f"GROUP: {group['id']} DOES NOT EXIT IN THE COMPARE FILE.")
            if group_comp['id'] == group['id']:
                diff = DeepDiff(group_comp, group)
                if diff:
                    errors.append(f"GROUP ID: {group_comp['id']} DOES NOT MATCH {diff}")

    for field_comp in match_form_compare['fields']:
        for field in full_res['fields']:
            if not field['id'] in comp_field_id_list:
                errors.append(f"FIELD: {field['id']} DOES NOT EXIT IN THE COMPARE FILE.")
            if field_comp['id'] == field['id']:
                diff = DeepDiff(field_comp, field)
                if diff:
                    errors.append(f"FIELD ID: {field_comp['id']} DOES NOT MATCH {diff}")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))            
