import pytest
import json

from fastapi import HTTPException
from starlette.config import environ
from gearbox.models import StudyAlgorithmEngine, StudyVersion

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

TEST_CREATE_LIST = [
        {
            "study_algorithm_engine": {
                "algorithm_logic": None
            },
            "test": "create_new_study_algorithm_engine",
            "logic_file": "./tests/data/new_algorithm_logic.json",
            "study_version_id": 7
        },
        {
                "study_algorithm_engine": {
            "algorithm_logic": None,
            "study_version_id": 7,
            "id": 7
                },
            "logic_file": "./tests/data/update_algorithm_logic.json",
            "test": "update_new_study_algorithm_engine"
        }
        ,
        {
                "study_algorithm_engine": {
            "algorithm_logic": None
                },
            "study_version_id": 1,
            "logic_file": "./tests/data/new_algorithm_logic.json",
            "test": "invalid_study_version"
        },
        {
                "study_algorithm_engine": {
            "algorithm_logic": None
                },
            "study_version_id": 1,
            "logic_file": "./tests/data/algorithm_logic.json",
            "test": "duplicate_logic"
        },
        {
                "study_algorithm_engine": {
            "algorithm_logic": None
                },
            "study_version_id": 1,
            "active": True,
            "logic_file": "./tests/data/algorithm_logic_invalid_el_criteria_has_criterion_ids.json",
            "test":"invalid_criteria_ids"
        }
        ,
        {
                "study_algorithm_engine": {
            "algorithm_logic": None
                },
            "active": True,
            "study_version_id": 1,
            "logic_file": "./tests/data/algorithm_logic_invalid_schema.json",
            "test":"invalid_logic"
        }
]


@pytest.mark.parametrize('test_create_data',TEST_CREATE_LIST)
def test_create_study_algorithm_engine(setup_database, client, test_create_data, connection):
    """
    Comments:
    This test performs the following tests on the study-algorithm-engine post endpoint
    1.) "create_new_study_algorithm_engine" - create new algorithm_engine table row 
    2.) "invalid_study_version" - invalid study version returns a 500 response code
    3.) "duplicate_logic" - finds duplicate row, sets status to active
    4.)  "invalid_criteria_ids" - 500 response code and produces a list of invalid criterion ids
    5.)  "invalid_logic" - fails json schema validation 
    """

    fake_jwt = "1.2.3"

    logic_file = test_create_data['logic_file']
    with open(logic_file, 'r') as comp_file:
        ae_logic_json = comp_file.read().replace('\n','').replace('\t',' ')

    data = {}
    data = {
        "algorithm_logic" : ae_logic_json
    }

    if test_create_data["test"] == "update_new_study_algorithm_engine":
        # Set the id to update
        data['id'] = test_create_data['study_algorithm_engine']['id']
        data['algorithm_logic'] = ae_logic_json
        data['study_version_id'] = test_create_data['study_algorithm_engine']['study_version_id']

        resp = client.post("/update-study-algorithm-engine", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
        pass
    else:
        data['study_version_id'] = test_create_data['study_version_id']
        resp = client.post("/study-algorithm-engine", json=data, headers={"Authorization": f"bearer {fake_jwt}"})

    errors = []
    # TEST NEW STUDY ALGORITHM ENGINE SUCCESS
    if test_create_data["test"] == "create_new_study_algorithm_engine":
        if not (str(resp.status_code).startswith("20")):
            errors.append(f"ERROR: create_new_study_algorithm_engine test: unexpected http status in response: {str(resp.status_code)}")
        full_res = resp.json()
        new_ae_id = full_res['id']
        # verify row created 
        try:
            Session = sessionmaker(bind=connection)
            db_session = Session()

            stmt = select(StudyAlgorithmEngine.algorithm_logic, StudyAlgorithmEngine.id).where(StudyAlgorithmEngine.id == new_ae_id)
            ael = db_session.execute(stmt).first()
            if not ael:
                errors.append(f"ERROR: create_new_study_algorithm_engine test failed to confirm new study_algorithm_engine row created.")

            # compare db json against input file
            with open(logic_file, 'r') as comp_file:
                ae_logic_json = json.loads(comp_file.read())
            if not ae_logic_json == ael.algorithm_logic:
                errors.append(f"ERROR: create_new_study_algorithm_engine test db algorithm_logic does not match input data.")

            stmt = select(StudyVersion.study_algorithm_engine_id).where(StudyVersion.study_algorithm_engine_id == new_ae_id)
            sv = db_session.execute(stmt).first()
            if not sv:
                errors.append(f"ERROR: create_new_study_algorithm_engine test failed to confirm updated study_version row for new study_algorithm_engine.")

            db_session.close()
        except Exception as e:
            errors.append(f"SQL ERROR: create_new_study_algorithm_engine: {e}")

    elif test_create_data["test"] == "update_new_study_algorithm_engine":
        if not (str(resp.status_code).startswith("20")):
            errors.append(f"ERROR: update_new_study_algorithm_engine test: unexpected http status in response: {str(resp.status_code)}")
        full_res = resp.json()

        # returns duplicate (existing) row with updated status
        new_ae_id = full_res['id']
        # verify row created 
        try:
            Session = sessionmaker(bind=connection)
            db_session = Session()

            stmt = select(StudyAlgorithmEngine.algorithm_logic, StudyAlgorithmEngine.id).where(StudyAlgorithmEngine.id == new_ae_id)
            ael = db_session.execute(stmt).first()
            if not ael:
                errors.append(f"ERROR: create_new_study_algorithm_engine test failed to confirm new study_algorithm_engine row created.")

            # compare db json against input file
            with open(logic_file, 'r') as comp_file:
                ae_logic_json = json.loads(comp_file.read())
            if not ae_logic_json == ael.algorithm_logic:
                errors.append(f"ERROR: create_new_study_algorithm_engine test db algorithm_logic does not match input data.")
            db_session.close()
        except Exception as e:
            errors.append(f"SQL ERROR: create_new_study_algorithm_engine: {e}")

    # TEST INVALID STUDY
    elif test_create_data["test"] == "invalid_study_version":
        if not (str(resp.status_code).startswith("50")):
            errors.append(f"ERROR: invalid_study_version unexpected http status in response: {str(resp.status_code)}")

    # TEST INVALID CRITERIA
    elif test_create_data["test"] == "invalid_criteria_ids":
        if not (str(resp.status_code).startswith("50")):
            errors.append(f"ERROR: invalid_criteria_ids unexpected http status in response: {str(resp.status_code)}")

    # TEST DUPLICATE algorithm_logic
    # this tests a new algorithm_version (2) that is an exact duplicate of version 1 (inactive)
    elif test_create_data["test"] == "duplicate_logic":
        if not (str(resp.status_code).startswith("20")):
            errors.append(f"ERROR: duplicate_logic test unexpected http status in response: {str(resp.status_code)}")
        full_res = resp.json()
        # returns duplicate (existing) row with updated status
        new_ae_id = full_res['id']
        # verify row created 
        try:
            Session = sessionmaker(bind=connection)
            db_session = Session()

            stmt = select(StudyAlgorithmEngine.algorithm_logic, StudyAlgorithmEngine.id).where(StudyAlgorithmEngine.id == new_ae_id)
            ael = db_session.execute(stmt).first()
            if not ael:
                errors.append(f"ERROR: duplicate_logic test failed to confirm new study_algorithm_engine row created.")

            # compare db json against input file
            with open(logic_file, 'r') as comp_file:
                ae_logic_json = json.loads(comp_file.read())
            if not ae_logic_json == ael.algorithm_logic:
                errors.append(f"ERROR: duplicate_logic test algorithm_logic does not match input data.")
            db_session.close()

        except Exception as e:
            errors.append(f"ERROR: duplicate_logic test: {e}")

    # TEST MALFORMED ALGORITHM LOGIC 
    elif test_create_data["test"] == "invalid_logic":
        if not (str(resp.status_code).startswith("4")):
            errors.append(f"ERROR: invalid_logic test unexpected http status in response: {str(resp.status_code)}")


    assert not errors, "errors occurred: \n{}".format("\n".join(errors))  

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

def test_get_algorithm_engines(setup_database, client):
    """
    Test that the algorithm-engine endpoint returns a 200 and valid json
    """
    fake_jwt = "1.2.3"
    resp = client.get("/study-algorithm-engines", headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    full_res = resp.json()
    al = full_res['results'][0]['algorithm_logic']

    # check algorithm_logic not empty
    assert al != ''
