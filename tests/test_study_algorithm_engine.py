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

@respx.mock
@pytest.mark.parametrize(
    "data", [ 
        {
            "study_version_id": 1,
            "algorithm_logic": None,
            "algorithm_version": 1,
            "active": True
        }
    ]
)
@pytest.mark.asyncio
def test_create_study_algorithm_engine(setup_database, client, data, connection):
    """
    Comments:
    This test performs the following:
    1.) Creates a new row in the study_algorithm_engine table 
    2.) Validates that that new row was created
    3.) Validates that the json stored in the algorithm_logic column matches the input data
    4.) Deletes the test row from the study_algorithm_engine table
    """

    print("--------------------------> STARTING test create --------------------------->")
    ae_file = './tests/data/algorithm_logic.json'
    with open(ae_file, 'r') as comp_file:
        ae_json = comp_file.read().replace('\n','').replace('\t',' ')
    data['algorithm_logic'] = ae_json
    fake_jwt = "1.2.3"
    resp = client.post("/study-algorithm-engine", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    full_res = resp.json()
    # print(f"FULL RESPONSE: {full_res}")
    new_ae_id = full_res['id']
    print(f"------------ NEW ID: {new_ae_id}")
    print(f"------------ NEW LOGIC: {full_res['algorithm_logic']}")

    errors = []
    if not (str(resp.status_code).startswith("20")):
        errors.append(f"ERROR bad http status in response: {str(resp.status_code)}")

    try:
        Session = sessionmaker(bind=connection)
        db_session = Session()

        print("QUERY ------------------")
        print(f"{db_session.query(StudyAlgorithmEngine.algorithm_logic).filter(StudyAlgorithmEngine.id==new_ae_id)}")
        ael = db_session.query(StudyAlgorithmEngine.algorithm_logic).filter(StudyAlgorithmEngine.id==new_ae_id).all()
        ael = json.dumps(ael)
        print("-----------------------------------------------------")
        print(f"AEL: {ael}")
        print(f"data algorithm_logic: {data['algorithm_logic']}")
        print("-----------------------------------------------------")

        if not (ael == data['algorithm_logic']):
            errors.append("JSON does not match...")

        # cleanup
        # db_session.query(StudyAlgorithmEngine).filter(StudyAlgorithmEngine.id==new_ae_id).delete()
        db_session.commit()
        db_session.close()
    except Exception as e:
        print("SQL EXCEPTION DURING CLEANUP")

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
    print(f"FULL RES: {full_res}")
    al = full_res['algorithm_logic']

    # check algorithm_logic not empty
    assert al != ''