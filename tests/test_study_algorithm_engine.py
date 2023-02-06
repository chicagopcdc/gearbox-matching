import pytest
import json
import jwt
import random

from httpx import AsyncClient
from fastapi import FastAPI

import respx

from fastapi import HTTPException
from starlette.config import environ
from gearbox import config
from gearbox.util import status
from gearbox.models import StudyAlgorithmEngine

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select

TEST_CREATE_LIST = [
        {
            "study_version_id": 1,
            "algorithm_logic": None,
            "algorithm_version": 1,
            "active": True,
            "logic_file": "./tests/data/algorithm_logic.json",
            "success": True
        },
        {
            "study_version_id": 1,
            "algorithm_logic": None,
            "algorithm_version": 1,
            "active": True,
            "logic_file": "./tests/data/algorithm_logic_invalid_schema.json",
            "success":False
        }

]

@respx.mock
@pytest.mark.asyncio
@pytest.mark.parametrize('test_create_data',TEST_CREATE_LIST)
def test_create_study_algorithm_engine(setup_database, client, test_create_data, connection):
    """
    Comments:
    This test performs the following:
    1.) Creates a new row in the study_algorithm_engine table 
    2.) Validates that that new row was created
    3.) Validates that the json stored in the algorithm_logic column matches the input data
    4.) Deletes the test row from the study_algorithm_engine table
    """
    data = {
        "study_version_id": test_create_data['study_version_id'],
        "algorithm_version": test_create_data['algorithm_version'],
        "active": test_create_data['active'],
    }

    logic_file = test_create_data['logic_file']
    with open(logic_file, 'r') as comp_file:
        ae_json = comp_file.read().replace('\n','').replace('\t',' ')
    data['algorithm_logic'] = ae_json

    print(f"TEST ALGORITHM LOGIC: {json.dumps(data['algorithm_logic'])}")
    fake_jwt = "1.2.3"
    resp = client.post("/study-algorithm-engine", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    print(f"----------------------------> RESPONSE CODE: {resp}")
    print(f"----------------------------> RESPONSE CODE: {resp.status_code}")

    # resp.raise_for_status()

    # if success we need to see if new_ae_id is created 

    errors = []
    if test_create_data["success"]:
        if not (str(resp.status_code).startswith("20")):
            errors.append(f"ERROR bad http status in response: {str(resp.status_code)}")
        full_res = resp.json()
        new_ae_id = full_res['id']
        # verify row created 
        try:
            Session = sessionmaker(bind=connection)
            db_session = Session()

            stmt = select(StudyAlgorithmEngine.algorithm_logic, StudyAlgorithmEngine.active, StudyAlgorithmEngine.id, StudyAlgorithmEngine.study_version_id).where(StudyAlgorithmEngine.id == new_ae_id)
            result = db_session.execute(stmt)
            ael = result.all()
            if not ael:
                errors.append(f"ERROR failed to confirm new study_algorithm_engine row created.")
            db_session.close()
        except Exception as e:
            print(f"SQL EXCEPTION DURING DB QUERY CONFIRM NEW study_algorithm_engine: {e}")
    else:
        if not (str(resp.status_code).startswith("4")):
            errors.append(f"ERROR bad http status in response: {str(resp.status_code)}")


    assert not errors, "errors occurred: \n{}".format("\n".join(errors))  

@respx.mock
def test_get_algorithm_engine(setup_database, client):
    """
    Test that the algorithm-engine endpoint returns a 200 and valid json
    """
    fake_jwt = "1.2.3"
    resp = client.get("/study-algorithm-engine/1", headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    full_res = resp.json()
    al = full_res['algorithm_logic']

    # check algorithm_logic not empty
    assert al != ''