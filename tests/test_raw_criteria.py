import pytest
import json
from sqlalchemy.orm import sessionmaker 
from gearbox.models import CriterionStaging, StudyVersion, StudyExternalId, Study
from .test_utils import is_aws_url
from sqlalchemy import select
from gearbox.util.types import AdjudicationStatus, StudyVersionStatus


@pytest.mark.asyncio
def test_get_raw_criteria_by_ec(setup_database, client):
    """
    Comments: Test to get raw_criteria by eligibility_criteria id
    """
    fake_jwt = "1.2.3"
    resp = client.get("/raw-criteria-ec/1", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

@pytest.mark.asyncio
def test_get_raw_criteria_by_id(setup_database, client):
    """
    Comments: Test to get raw_criteria by raw_criteria id
    """
    fake_jwt = "1.2.3"
    resp = client.get("/raw-criteria/1", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

@pytest.mark.asyncio
def test_create_raw_criteria(setup_database, client):
       
    fake_jwt = "1.2.3"
    test_raw_crit = "./tests/data/test_raw_criteria.json"
    with open(test_raw_crit, 'r') as test_raw_crit_file:
        raw_crit_data = test_raw_crit_file.read()
    
    raw_crit_data = json.loads(raw_crit_data)
    resp = client.post("/raw-criteria", json=raw_crit_data, headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

@pytest.mark.asyncio
def test_create_raw_criteria_invalid_nct_id(setup_database, client):
       
    fake_jwt = "1.2.3"
    test_raw_crit = "./tests/data/test_raw_criteria_invalid_nct_id.json"
    with open(test_raw_crit, 'r') as test_raw_crit_file:
        raw_crit_data = test_raw_crit_file.read()
    
    raw_crit_data = json.loads(raw_crit_data)
    resp = client.post("/raw-criteria", json=raw_crit_data, headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("50")

@pytest.mark.asyncio
def test_create_raw_criteria_invalid_schema(setup_database, client):
       
    fake_jwt = "1.2.3"
    test_raw_crit = "./tests/data/test_raw_criteria_invalid_schema.json"
    with open(test_raw_crit, 'r') as test_raw_crit_file:
        raw_crit_data = test_raw_crit_file.read()
    
    raw_crit_data = json.loads(raw_crit_data)
    resp = client.post("/raw-criteria", json=raw_crit_data, headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("422")

@pytest.mark.asyncio
def test_create_raw_criteria_reupload(setup_database, client, connection):
    """
    This test simulates a re-upload of raw criteria from doccano for
    a study_version that currently exists in "IN_PROCESS" or "NEW" status.

    """
    errors = []   
    fake_jwt = "1.2.3"
    test_raw_crit = "./tests/data/test_raw_criteria_reupload.json"
    with open(test_raw_crit, 'r') as test_raw_crit_file:
        raw_crit_data = test_raw_crit_file.read()
    
    raw_crit_data = json.loads(raw_crit_data)
    resp = client.post("/raw-criteria", json=raw_crit_data, headers={"Authorization": f"bearer {fake_jwt}"})
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Raw-criteria re-upload first post failed: {resp.status_code}")

    test_raw_crit = "./tests/data/test_raw_criteria_reupload_with_changes.json"
    with open(test_raw_crit, 'r') as test_raw_crit_file:
        raw_crit_data = test_raw_crit_file.read()
    
    raw_crit_data = json.loads(raw_crit_data)
    resp = client.post("/raw-criteria", json=raw_crit_data, headers={"Authorization": f"bearer {fake_jwt}"})
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Raw-criteria re-upload second post failed: {resp.status_code}")

    try:
        Session = sessionmaker(bind=connection)
        db_session = Session()

        stmt = select(CriterionStaging.id).where(
            CriterionStaging.code == 'new_criteria_for_reload_test').where(
            CriterionStaging.criterion_adjudication_status == AdjudicationStatus.NEW
        )
        cs = db_session.execute(stmt).first()
        if not cs:
            errors.append("new_criteria_for_reload_test new criterion code not found in criterion_staging")

        stmt = select(CriterionStaging.id).where(
            CriterionStaging.code == 'meas_dlco').where(
            CriterionStaging.eligibility_criteria_id == 18).where(
            CriterionStaging.criterion_adjudication_status == AdjudicationStatus.EXISTING).where(
            CriterionStaging.text == "DLCO-TEST-EXISTING-TEXT-CHANGE ≥ 40%"
        )

        cs = db_session.execute(stmt).first()
        if not cs:
            errors.append("Updated criterion code not found in criterion_staging")

        stmt = select(CriterionStaging.id).where(
            CriterionStaging.code == 'meas_dlco').where(
            CriterionStaging.eligibility_criteria_id == 18).where(
            CriterionStaging.criterion_adjudication_status == AdjudicationStatus.INACTIVE).where(
            CriterionStaging.text == "DLCO ≥ 40%"
        )

        cs = db_session.execute(stmt).first()
        if not cs:
            errors.append("Obsolete criterion code not found in criterion_staging")
        
    except Exception as ex:
        errors.append(f"SQL ERROR: create_raw_criteria_reload test: {ex}")

    assert not errors

@pytest.mark.asyncio
def test_create_raw_criteria_reupload_exact_dup(setup_database, client, connection):
    """
    This test simulates a re-upload of raw criteria from doccano for
    a study_version that currently exists in "IN_PROCESS" or "NEW" status.

    """
    errors = []   
    fake_jwt = "1.2.3"
    test_raw_crit = "./tests/data/test_raw_criteria_exact_dup.json"
    with open(test_raw_crit, 'r') as test_raw_crit_file:
        raw_crit_data = test_raw_crit_file.read()
    
    raw_crit_data = json.loads(raw_crit_data)
    resp = client.post("/raw-criteria", json=raw_crit_data, headers={"Authorization": f"bearer {fake_jwt}"})
    # load exact dup
    resp = client.post("/raw-criteria", json=raw_crit_data, headers={"Authorization": f"bearer {fake_jwt}"})

    try:
        Session = sessionmaker(bind=connection)
        db_session = Session()
        """
        Based on input data, study NCT05188170 should have exactly one row
        in IN_PROCESS status.
        """
        stmt = select(StudyVersion).join(StudyVersion.study).join(StudyExternalId).where(
            StudyExternalId.ext_id == 'NCT05188170').where(
                StudyVersion.status == StudyVersionStatus.IN_PROCESS)
        svs = db_session.execute(stmt).unique()
        sv_rows_returned = len(svs.all())
        
        if sv_rows_returned != 1:
            errors.append(f"Raw-criteria exact dup re-upload test failed returned {sv_rows_returned} rows. Expecting one row.")

    except Exception as ex:
        errors.append(f"SQL ERROR: create_raw_criteria_reload test: {ex}")
    assert not errors