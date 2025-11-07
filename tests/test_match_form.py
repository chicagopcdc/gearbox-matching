import json
from .test_utils import is_aws_url
import pytest

from sqlalchemy.orm import sessionmaker
from gearboxdatamodel.models import Value, Unit

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

def test_get_important_questions(setup_database, client):
    errors = []
    fake_jwt = "1.2.3"
    url = client.get("/important-questions", headers={"Authorization": f"bearer {fake_jwt}"})
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

def test_update_match_form_new_value(setup_database, client, connection):
    errors = []
    fake_jwt = "1.2.3"
    matchformdata_file = './tests/data/match_form_update_compare_dat_new_value_input.json'
    with open(matchformdata_file, 'r') as comp_file:
        match_form_for_update = json.load(comp_file)
    resp = client.post("/update-match-form", json=match_form_for_update, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")
    resp = client.post("/build-match-form/", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

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

    try:
        # Validate new db rows for value and unit
        Session = sessionmaker(bind=connection)
        db_session = Session()
        newval = db_session.query(Value).filter(Value.value_string=='99999999').first()
        if not newval: errors.append("Value: '99999999' not created")
        newunit = db_session.query(Unit).filter(Unit.name=='some_new_unit').first()
        if not newunit: errors.append("Unit: 'some_new_unit' not created")

    except Exception as e:
        print(f"Problem validating new rows in test update match form with new values: {e}")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))   

def test_update_match_form_new_value_existing_unit(setup_database, client, connection):
    errors = []
    fake_jwt = "1.2.3"
    matchformdata_file = './tests/data/match_form_update_compare_dat_new_value_existing_unit_input.json'
    with open(matchformdata_file, 'r') as comp_file:
        match_form_for_update = json.load(comp_file)

    resp = client.post("/update-match-form", json=match_form_for_update, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")
    resp = client.post("/build-match-form/", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    resp.raise_for_status()
    matchformdata_file = './tests/data/match_form_update_compare_dat_new_value_existing_unit.json'

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

    try:
        # Validate new db rows for value and unit
        Session = sessionmaker(bind=connection)
        db_session = Session()
        newval = db_session.query(Value).filter(Value.value_string=='89999999.0').first()
        if not newval: errors.append("Value: '89999999' not created")
        newunit = db_session.query(Unit).filter(Unit.name=='years').first()
        if not newunit: errors.append("Unit: 'some_new_unit' not created")

    except Exception as e:
        print(f"Problem validating new rows in test update match form with new values: {e}")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))   

def test_update_match_form_new_value_invalid_number(setup_database, client, connection):
    errors = []
    fake_jwt = "1.2.3"
    matchformdata_file = './tests/data/match_form_update_compare_dat_new_value_input_bad_number.json'
    with open(matchformdata_file, 'r') as comp_file:
        match_form_for_update = json.load(comp_file)

    resp = client.post("/update-match-form", json=match_form_for_update, headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == HTTP_500_INTERNAL_SERVER_ERROR

def test_update_match_form_new_field(setup_database, client):
    errors = []
    fake_jwt = "1.2.3"
    matchformdata_file = './tests/data/match_form_update_new_field.json'
    with open(matchformdata_file, 'r') as comp_file:
        match_form_for_update = json.load(comp_file)

    resp = client.post("/update-match-form", json=match_form_for_update, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")

    resp = client.post("/build-match-form/", headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    full_res = resp.json()

    #""" SERIALIZE STUDIES TO COMPARE AGAINST - UNCOMMENT TO WRITE NEW COMPARE DATA
    #    MANUALLY VALIDATE MATCH FORM BEFORE UNCOMMENTING 
    #with open(matchformdata_file,'w') as comp_file:
    #    json.dump(full_res, comp_file)
    #"""

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
