import pytest
import json
import jwt
import random

from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

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
        session = Session()
        crit = session.query(Criterion).filter(Criterion.code==test_criterion_code).first()
        if not crit: errors.append("CRITERION: {test_criterion_code} not created")

        chv = session.query(CriterionHasValue).filter(CriterionHasValue.criterion_id==crit.id).all()
        if not chv: errors.append("CRITERION CRITERION HAS VALUE FOR CRITERION CODE: {test_criterion_code} not created")

        cht = session.query(CriterionHasTag).filter(CriterionHasTag.criterion_id==crit.id).all()
        if not cht: errors.append("CRITERION CRITERION HAS TAG FOR CRITERION CODE: {test_criterion_code} not created")

        dr = session.query(DisplayRules).filter(DisplayRules.criterion_id==crit.id).first()
        if not cht: errors.append("CRITERION CRITERION HAS TAG FOR CRITERION CODE: {test_criterion_code} not created")

        tb = session.query(TriggeredBy).filter(TriggeredBy.criterion_id==crit.id).first()
        if not tb: errors.append("CRITERION TRIGGERED BY FOR CRITERION CODE: {test_criterion_code} not created")

        # cleanup
        d = session.query(CriterionHasValue).filter(CriterionHasValue.criterion_id==crit.id).delete()
        d = session.query(CriterionHasTag).filter(CriterionHasTag.criterion_id==crit.id).delete()
        d = session.query(DisplayRules).filter(DisplayRules.criterion_id==crit.id).delete()
        d = session.query(TriggeredBy).filter(DisplayRules.criterion_id==crit.id).delete()
        d = session.query(Criterion).filter(Criterion.id==crit.id).delete()
        session.commit()
        session.close()
    except Exception as e:
        print(f"Exception creating new criterion: {e}")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

# TO DO: create test for violating unique constraint
"""
@respx.mock
def test_get_values(client):
    fake_jwt = "1.2.3"
    resp = client.get("/criteria", headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == 200
"""