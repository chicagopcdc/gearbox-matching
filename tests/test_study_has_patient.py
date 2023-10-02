import pytest
import random
import json

from sqlalchemy.orm import sessionmaker
from gearbox.models import StudyHasPatient
from deepdiff import DeepDiff

from .test_utils import is_aws_url

# test to validate StudyHasPatient endpoints are enabled
@pytest.mark.asyncio
def test_get_study_has_patients(setup_database, client):
    """
    Comments: Test to validate StudyHasPatient endpoints are enabled
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/study-has-patients", headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")

# test to validate StudyHasPatient endpoints transfer data accurately
@pytest.mark.asyncio
def test_study_has_patients_compare(setup_database, client):
    """
    Comments: This test builds the study_has_patient document and compares vs study_has_patients.json 
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/study-has-patients", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    resp.raise_for_status()
    study_has_patientdata_file = './tests/data/study_has_patients.json'

    """ SERIALIZE STUDY_HAS_PATIENTS TO COMPARE AGAINST - UNCOMMENT TO WRITE NEW COMPARE DATA
    with open(study_has_patientdata_file,'w') as comp_file:
        json.dump(full_res, comp_file)
    """

    with open(study_has_patientdata_file, 'r') as comp_file:
        study_has_patient_compare = json.load(comp_file)

    study_has_patients = full_res["results"]
    study_has_patient_compare = study_has_patient_compare["results"]

    diff = []
    # Diff all study_has_patients in the reponse that exist in the mock file
    for i in range (len(study_has_patient_compare)):
        study_has_patient_diff = DeepDiff(study_has_patients[i], study_has_patient_compare[i], ignore_order=True)
        if (study_has_patient_diff):
            diff.append(study_has_patient_diff)
    
    assert not diff, "differences occurred: \n{}".format("\n".join(diff))

# test to validate StudyHasPatient endpoints create entries in the database
# by creating a new study_has_patient entry in the database
@pytest.mark.asyncio
def test_study_has_patients_create(setup_database, client):
    """
    Comments: This test creates a new study_has_patient entry in the database
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/study-has-patients", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    resp.raise_for_status()
    study_has_patientdata_file = './tests/data/study_has_patients.json'

    """ SERIALIZE STUDY_HAS_PATIENTS TO COMPARE AGAINST - UNCOMMENT TO WRITE NEW COMPARE DATA
    with open(study_has_patientdata_file,'w') as comp_file:
        json.dump(full_res, comp_file)
    """

    with open(study_has_patientdata_file, 'r') as comp_file:
        study_has_patient_compare = json.load(comp_file)

    study_has_patients = full_res["results"]
    study_has_patient_compare = study_has_patient_compare["results"]

    diff = []
    # Diff all study_has_patients in the reponse that exist in the mock file
    for i in range (len(study_has_patient_compare)):
        study_has_patient_diff = DeepDiff(study_has_patients[i], study_has_patient_compare[i], ignore_order=True)
        if (study_has_patient_diff):
            diff.append(study_has_patient_diff)
    
    assert not diff, "differences occurred: \n{}".format("\n".join(diff))
