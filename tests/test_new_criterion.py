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

@respx.mock
@pytest.mark.parametrize(
    "data", [ 
    {       
        "code": "test_criteria",
        "display_name": "this is a test criteria",
        "description": "this is a test criteria",
        "active": False,
        "input_type_id": 1,
        "tags": [1],
        "values": [3],
        "display_rules_priority": 1001,
        "display_rules_version": 5,
        "triggered_by_criterion_id": 1,
        "triggered_by_value_id": 1,
        "triggered_by_path": "2.3.4"
    }
    ]
)
@pytest.mark.asyncio
def test_create_criterion(client, valid_upload_file_patcher, data, connection):
    """
    Test create /user-input response for a valid user with authorization and
    valid input, ensure correct response.
    """
    errors=[]
    fake_jwt = "1.2.3"
    test_criterion_code = 'PYTEST TESTCODE' + str(random.randint(0,9999))
    data['code'] = test_criterion_code
    resp = client.post("/criterion", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
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

        tb = db_session.query(TriggeredBy).filter(TriggeredBy.value_id==data['triggered_by_value_id']).first()
        if not tb: errors.append("CRITERION TRIGGERED BY FOR CRITERION CODE: {test_criterion_code} not created")

        dr = db_session.query(DisplayRules).filter(DisplayRules.criterion_id==crit.id).first()
        if not cht: errors.append("CRITERION CRITERION HAS TAG FOR CRITERION CODE: {test_criterion_code} not created")

        # cleanup
        d = db_session.query(CriterionHasValue).filter(CriterionHasValue.criterion_id==crit.id).delete()
        d = db_session.query(CriterionHasTag).filter(CriterionHasTag.criterion_id==crit.id).delete()
        d = db_session.query(TriggeredBy).filter(TriggeredBy.criterion_id==data['triggered_by_value_id']).delete()
        d = db_session.query(DisplayRules).filter(DisplayRules.criterion_id==crit.id).delete()
        d = db_session.query(Criterion).filter(Criterion.id==crit.id).delete()
        db_session.commit()
        db_session.close()
    except Exception as e:
        print(f"Exception validating new criterion: {e}")
        errors.append(str(e))

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

@pytest.mark.asyncio
def test_create_criterion_fail_triggered_by(client, valid_upload_file_patcher, mock_new_criterion, connection):
    """
    Test create /user-input response for a valid user with authorization and
    valid input, ensure correct response.
    """
    errors=[]
    fake_jwt = "1.2.3"
    test_criterion_code = 'PYTEST TESTCODE' + str(random.randint(0,9999))
    mock_new_criterion.triggered_by_value_id = None
    mock_json = mock_new_criterion.to_json()
    resp = client.post("/criterion", json=mock_new_criterion.to_json(), headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == 500 

# TO DO: create test for violating unique constraint,
# TO DO: test if no triggered_by exists in input dict 

"""
@respx.mock
def test_get_values(client):
    fake_jwt = "1.2.3"
    resp = client.get("/criteria", headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == 200
"""
# TO DO: create test for violating unique constraint,