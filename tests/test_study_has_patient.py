import pytest
import json
from deepdiff import DeepDiff
from gearbox.deps import get_session

from fastapi.testclient import TestClient
import importlib
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from gearboxdatamodel.models import StudyHasPatient, Study

@pytest.fixture(scope="session")
def database(setup_database) -> Engine:
    session = setup_database

    yield session

    session.query(StudyHasPatient).delete()
    study_1 = session.query(Study).filter(Study.name == 'study 1').delete()
    study_2 = session.query(Study).filter(Study.name == 'study 2').delete()
    study_3 = session.query(Study).filter(Study.name == 'study 3').delete()
    session.commit()
    session.close()

@pytest.fixture(scope="session")
def add_study_simple(database):

    study_1 = Study(
         name='study 1',
         code='ADDSTUDYSIMPLECODE 1'
     )

    database.add(study_1)
    database.commit()

    study_id = database.query(Study.id).filter(Study.name == 'study 1').first()[0]

    study_patient_1_1 = StudyHasPatient(
        study_id=study_id,
        patient_id="1",
        data={
            f"{study_id}": 1
        },
        source_id="test.com"
     )
    
    database.add(study_patient_1_1)
    database.commit()

    yield study_id

@pytest.fixture(scope="session")
def add_study_complex(database):
    study_2 = Study(
         name='study 2',
         code='ADDSTUDYSIMPLECODE 2'
     )

    study_3 = Study(
         name='study 3',
         code='ADDSTUDYSIMPLECODE 3'
    )
    
    database.add_all([study_2, study_3])
    database.commit()

    study_id_2 = database.query(Study.id).filter(Study.name == 'study 2').first()[0]
    study_id_3 = database.query(Study.id).filter(Study.name == 'study 3').first()[0]


    study_patient_2_1 = StudyHasPatient(
        study_id=study_id_2,
        patient_id="1",
        data={
            f"{study_id_2}": 1
        },
        source_id="test.com"
     )
    
    study_patient_2_2 = StudyHasPatient(
        study_id=study_id_2,
        patient_id="2",
        data={
            f"{study_id_2}": 2
        },
        source_id="test.com"
     )
    
    study_patient_3_1 = StudyHasPatient(
        study_id=study_id_3,
        patient_id="1",
        data={
            f"{study_id_3}": 1
        },
        source_id="test.com"
     )
    
    study_patient_3_2 = StudyHasPatient(
        study_id=study_id_3,
        patient_id="2",
        data={
            f"{study_id_3}": 2
        },
        source_id="test.com"
     )
    
    study_patient_3_3 = StudyHasPatient(
        study_id=study_id_3,
        patient_id="3",
        data={
            f"{study_id_3}": 3
        },
        source_id="test.com"
     )
    
    database.add_all([study_patient_2_1, study_patient_2_2, study_patient_3_1, study_patient_3_2, study_patient_3_3])
    database.commit()

    yield study_id_2, study_id_3


# test to validate StudyHasPatient endpoints are enabled
@pytest.mark.asyncio
def test_get_study_has_patients_simple(add_study_simple, client):
    """
    Comments: Test one study and one patient
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get(f"/study-has-patients?study_id={add_study_simple}", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")
    assert resp.json() == [{
        "study_id": add_study_simple,
        "patient_id": "1",
        "data": {
            f"{add_study_simple}": 1
        },
        "source_id": "test.com"
    }]


@pytest.mark.asyncio
def test_get_study_has_patients_complex(add_study_complex, client):
    """
    Comments: Test multi study and multi patients
    """
    study_id_2, study_id_3 = add_study_complex
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get(f"/study-has-patients?study_id={study_id_2}", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")
    assert resp.json() == [{
                            "study_id": study_id_2,
                            "patient_id": "1",
                            "data": {
                                f"{study_id_2}": 1
                            },
                            "source_id": "test.com"
                        },
                        {
                            "study_id": study_id_2,
                            "patient_id": "2",
                            "data": {
                                f"{study_id_2}": 2
                            },
                            "source_id": "test.com"
                        }]
    
    resp = client.get(f"/study-has-patients?study_id={study_id_3}", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")
    assert resp.json() == [{
                            "study_id": study_id_3,
                            "patient_id": "1",
                            "data": {
                                f"{study_id_3}": 1
                            },
                            "source_id": "test.com"
                        },
                        {
                            "study_id": study_id_3,
                            "patient_id": "2",
                            "data": {
                                f"{study_id_3}": 2
                            },
                            "source_id": "test.com"
                        },
                        {
                            "study_id": study_id_3,
                            "patient_id": "3",
                            "data": {
                                f"{study_id_3}": 3
                            },
                            "source_id": "test.com"
                        }]


@pytest.mark.asyncio
def test_get_patients_has_studies_complex(add_study_simple, add_study_complex, client):
    errors = []
    fake_jwt = "1.2.3"
    study_id_2, study_id_3 = add_study_complex
    resp = client.get(f"/patient-has-studies?patient_id='1'", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")
    assert resp.json() == [{
                            "study_id": add_study_simple,
                            "patient_id": "1",
                            "data": {
                                f"{add_study_simple}": 1
                            },
                            "source_id": "test.com"
                        },
                        {
                            "study_id": study_id_2,
                            "patient_id": "1",
                            "data": {
                                f"{study_id_2}": 1
                            },
                            "source_id": "test.com"
                        },
                        {
                            "study_id": study_id_3,
                            "patient_id": "1",
                            "data": {
                                f"{study_id_3}": 1
                            },
                            "source_id": "test.com"
                        }]
    
@pytest.mark.asyncio
def test_create_study_has_patients(add_study_simple, database, client):
    json_data = [{
                    "study_id": add_study_simple,
                    "patient_id": "4",
                    "data": {
                        f"{add_study_simple}": 1
                    },
                    "source_id": "test.com"
                }]
    
    fake_jwt = "1.2.3"
    resp = client.post("/study-has-patient", json=json_data, headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

    added_data = database.query(StudyHasPatient).filter(StudyHasPatient.patient_id == '4').first()

    assert added_data.study_id == add_study_simple
    assert added_data.patient_id == '4'

