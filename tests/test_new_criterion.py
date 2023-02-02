import pytest
import json
import jwt
import random

from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker, Session

from gearbox.models import Criterion, CriterionHasTag, CriterionHasValue, DisplayRules, TriggeredBy

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

@pytest.mark.asyncio
def test_get_criterion(setup_database, client, valid_upload_file_patcher, connection):

    fake_jwt = "1.2.3"
    criterion_id = 1

    resp = client.get(f"/criterion/{criterion_id}", headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")

@pytest.mark.asyncio
def test_create_criterion(setup_database, client, valid_upload_file_patcher, mock_new_criterion, connection):
    """
    Test create /user-input response for a valid user with authorization and
    valid input, ensure correct response.
    """
    errors=[]
    fake_jwt = "1.2.3"
    test_criterion_code = 'PYTEST TESTCODE' + str(random.randint(0,9999))
    mock_new_criterion.code = test_criterion_code
    # adding code to ensure unique display name
    mock_new_criterion.display_name += test_criterion_code
    resp = client.post("/criterion", json=mock_new_criterion.to_json(), headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()

        crit = db_session.query(Criterion).filter(Criterion.code==test_criterion_code).first()
        if not crit: errors.append("CRITERION: {test_criterion_code} not created")

        chv = db_session.query(CriterionHasValue).filter(CriterionHasValue.criterion_id==crit.id).all()
        if not chv: errors.append("CRITERION CRITERION HAS VALUE FOR CRITERION CODE: {test_criterion_code} not created")

        cht = db_session.query(CriterionHasTag).filter(CriterionHasTag.criterion_id==crit.id).all()
        if not cht: errors.append("CRITERION CRITERION HAS TAG FOR CRITERION CODE: {test_criterion_code} not created")

        tb = db_session.query(TriggeredBy).filter(TriggeredBy.value_id==mock_new_criterion.triggered_by_value_id).first()
        if not tb: errors.append("CRITERION TRIGGERED BY FOR CRITERION CODE: {test_criterion_code} not created")

        dr = db_session.query(DisplayRules).filter(DisplayRules.criterion_id==crit.id).first()
        if not cht: errors.append("CRITERION CRITERION HAS TAG FOR CRITERION CODE: {test_criterion_code} not created")

        # cleanup
        d = db_session.query(CriterionHasValue).filter(CriterionHasValue.criterion_id==crit.id).delete()
        d = db_session.query(CriterionHasTag).filter(CriterionHasTag.criterion_id==crit.id).delete()
        d = db_session.query(TriggeredBy).filter(TriggeredBy.criterion_id==mock_new_criterion.triggered_by_value_id).delete()
        d = db_session.query(DisplayRules).filter(DisplayRules.criterion_id==crit.id).delete()
        d = db_session.query(Criterion).filter(Criterion.id==crit.id).delete()
        db_session.commit()
        db_session.close()
    except Exception as e:
        errors.append(str(e))

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

@pytest.mark.asyncio
def test_create_criterion_fail_missing_criterion_code(setup_database, client, valid_upload_file_patcher, mock_new_criterion, connection):
    """
    Test create /user-input response for a valid user with authorization and
    valid input, ensure correct response.
    """
    errors=[]
    fake_jwt = "1.2.3"
    mock_new_criterion.code = None
    resp = client.post("/criterion", json=mock_new_criterion.to_json(), headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == 422

@pytest.mark.asyncio
def test_create_criterion_fail_triggered_by(setup_database, client, valid_upload_file_patcher, mock_new_criterion, connection):
    """
    Test create /user-input response for a valid user with authorization and
    valid input, ensure correct response.
    """
    errors=[]
    fake_jwt = "1.2.3"
    test_criterion_code = 'PYTEST TESTCODE' + str(random.randint(0,9999))
    mock_new_criterion.code = test_criterion_code
    mock_new_criterion.triggered_by_value_id = None
    resp = client.post("/criterion", json=mock_new_criterion.to_json(), headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == 500 

# TO DO: create test for violating unique constraint,
# TO DO: test if no triggered_by exists in input dict 

@pytest.mark.asyncio
def test_create_criterion_minimum_values_required(setup_database, client, valid_upload_file_patcher, mock_new_criterion, connection):
    """
    Test create /user-input response for a valid user with authorization and
    valid input, ensure correct response.
    """
    errors=[]
    fake_jwt = "1.2.3"
    test_criterion_code = 'PYTEST TESTCODE' + str(random.randint(0,9999))
    mock_new_criterion.code = test_criterion_code
    mock_new_criterion.description = None
    mock_new_criterion.active = None
    mock_new_criterion.values = None
    mock_new_criterion.display_rules_version = None
    mock_new_criterion.triggered_by_value_id = None
    mock_new_criterion.triggered_by_criterion_id = None
    mock_new_criterion.triggered_by_path = None
    # adding code to ensure unique display name
    mock_new_criterion.display_name += test_criterion_code

    resp = client.post("/criterion", json=mock_new_criterion.to_json(), headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()

        crit = db_session.query(Criterion).filter(Criterion.code==test_criterion_code).first()
        if not crit: errors.append("CRITERION: {test_criterion_code} not created")

        cht = db_session.query(CriterionHasTag).filter(CriterionHasTag.criterion_id==crit.id).all()
        if not cht: errors.append("CRITERION CRITERION HAS TAG FOR CRITERION CODE: {test_criterion_code} not created")

        dr = db_session.query(DisplayRules).filter(DisplayRules.criterion_id==crit.id).first()
        if not cht: errors.append("CRITERION CRITERION HAS TAG FOR CRITERION CODE: {test_criterion_code} not created")

        # cleanup
        d = db_session.query(CriterionHasTag).filter(CriterionHasTag.criterion_id==crit.id).delete()
        d = db_session.query(DisplayRules).filter(DisplayRules.criterion_id==crit.id).delete()
        d = db_session.query(Criterion).filter(Criterion.id==crit.id).delete()
        db_session.commit()
        db_session.close()
    except Exception as e:
        errors.append(str(e))

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

# TO DO: create test for violating unique constraint,