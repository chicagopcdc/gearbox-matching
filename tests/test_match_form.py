import json
from .test_utils import is_aws_url
import pytest

from deepdiff import DeepDiff
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
def test_build_match_form_no_save(setup_database, client):
    """
    Test create /match_form endpoint
    valid input, ensure correct response.
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.post("/build-match-form/?save=False", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    print(f"FULL RES: {json.dumps(full_res)}")

    resp.raise_for_status()

def test_build_match_form(setup_database, client):
    """
    Test create /match_form endpoint
    valid input, ensure correct response.
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.post("/build-match-form/", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    resp.raise_for_status()
    print(f"-------------------> RESPONSE STATUS: {resp.status_code}")

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

def test_get_match_form(setup_database, client):
    errors = []
    fake_jwt = "1.2.3"
    url = client.get("/match-form", headers={"Authorization": f"bearer {fake_jwt}"})
    url_str =  url.content.decode('ascii').strip('\"')

    assert is_aws_url(url_str)

def test_update_match_form(setup_database, client):
    errors = []
    fake_jwt = "1.2.3"
    matchformdata_file = './tests/data/match_form_update_compare_dat.json'
    with open(matchformdata_file, 'r') as comp_file:
        match_form_for_update = json.load(comp_file)

    resp = client.post("/update-match-form", json=match_form_for_update, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")
    # -- NEED TO SEND A MATCH-FORM WITH THE TEST! --
    # -- USE THE ONE IN THE DATA DIR --
    # url_str =  url.content.decode('ascii').strip('\"')
    resp = client.post("/build-match-form/", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    resp.raise_for_status()
    matchformdata_file = './tests/data/match_form_update_compare_dat.json'

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

def test_update_match_form_new_value(setup_database, client):
    errors = []
    fake_jwt = "1.2.3"
    matchformdata_file = './tests/data/match_form_update_compare_dat_new_value_input.json'
    with open(matchformdata_file, 'r') as comp_file:
        match_form_for_update = json.load(comp_file)

    resp = client.post("/update-match-form", json=match_form_for_update, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")
    # -- NEED TO SEND A MATCH-FORM WITH THE TEST! --
    # -- USE THE ONE IN THE DATA DIR --
    # url_str =  url.content.decode('ascii').strip('\"')
    resp = client.post("/build-match-form/", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    print(f"FULL RES: {json.dumps(full_res)}")

    resp.raise_for_status()
    matchformdata_file = './tests/data/match_form_update_compare_dat_new_value.json'

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