import pytest
import json
from sqlalchemy.orm import sessionmaker 
from gearbox.models import CriterionStaging, StudyVersion, StudyExternalId, EligibilityCriteria
from .test_utils import is_aws_url
from sqlalchemy import select, func
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
    test_raw_crit = "./tests/data/test_raw_criteria_create.zip"
    files = {'file': ('test_create_raw_criteria.zip', open(test_raw_crit, 'rb'), 'application/zip')}
    resp = client.post("/raw-criteria", files=files, headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

@pytest.mark.asyncio
def test_create_raw_criteria_invalid_nct_id(setup_database, client):
       
    fake_jwt = "1.2.3"
    test_raw_crit = "./tests/data/test_raw_criteria_invalid_nct_id.zip"
    files = {'file': ('test_raw_criteria_invalid_nct_id.zip', open(test_raw_crit, 'rb'), 'application/zip')}
    resp = client.post("/raw-criteria", files=files, headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("50")

@pytest.mark.asyncio
def test_create_raw_criteria_invalid_schema(setup_database, client):
       
    fake_jwt = "1.2.3"
    test_raw_crit = "./tests/data/test_raw_criteria_invalid_schema.zip"
    files = {'file': ('test_raw_criteria_invalid_schema.zip', open(test_raw_crit, 'rb'), 'application/zip')}
    resp = client.post("/raw-criteria", files=files, headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("422")

@pytest.mark.asyncio
def test_create_raw_criteria_reupload(setup_database, client, connection):
    """
    This test simulates a re-upload of raw criteria from doccano for
    a study_version that currently exists in "IN_PROCESS" or "NEW" status.

    """
    errors = []   
    fake_jwt = "1.2.3"
    test_raw_crit = "./tests/data/test_raw_criteria_reupload.zip"
    files = {'file': ('test_raw_criteria_reupload.zip', open(test_raw_crit, 'rb'), 'application/zip')}
    resp = client.post("/raw-criteria", files=files, headers={"Authorization": f"bearer {fake_jwt}"})
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Raw-criteria re-upload first post failed: {resp.status_code}")

    test_raw_crit = "./tests/data/test_raw_criteria_reupload_with_changes.zip"
    files = {'file': ('test_raw_criteria_reupload_with_changes.zip', open(test_raw_crit, 'rb'), 'application/zip')}
    resp = client.post("/raw-criteria", files=files, headers={"Authorization": f"bearer {fake_jwt}"})
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Raw-criteria re-upload second post failed: {resp.status_code}")

    try:
        Session = sessionmaker(bind=connection)
        db_session = Session()

        # fetch latest eligibility_criteria id
        stmt = select(func.max(EligibilityCriteria.id))
        res = db_session.execute(stmt)
        new_ec_id = res.scalar_one()

        stmt = select(CriterionStaging.id).where(
            CriterionStaging.code == 'new_criteria_for_reload_test').where(
            CriterionStaging.criterion_adjudication_status == AdjudicationStatus.NEW
        )
        cs = db_session.execute(stmt).first()
        if not cs:
            errors.append("new_criteria_for_reload_test new criterion code not found in criterion_staging")

        stmt = select(CriterionStaging.id).where(
            CriterionStaging.code == 'exp_anthracycline_ever').where(
            CriterionStaging.eligibility_criteria_id == new_ec_id).where(
            CriterionStaging.criterion_adjudication_status == AdjudicationStatus.EXISTING).where(
            CriterionStaging.text == "Xnthracycline"
        )

        cs = db_session.execute(stmt).first()
        if not cs:
            errors.append("Updated criterion code not found in criterion_staging")

        stmt = select(CriterionStaging.id).where(
            CriterionStaging.code == 'expression_flt3_itd').where(
            CriterionStaging.eligibility_criteria_id == new_ec_id).where(
            CriterionStaging.criterion_adjudication_status == AdjudicationStatus.INACTIVE)

        cs = db_session.execute(stmt).first()
        if not cs:
            errors.append("Obsolete criterion code not found in criterion_staging")

        # confirm pre_annotated_criterion and pre_annotated_criterion_model rows created    
        stmt = "SELECT count(*) from pre_annotated_criterion where raw_criteria_id=1"
        pac_ct = db_session.execute(stmt).scalar_one()
        if pac_ct != 184:
            errors.append(f"Error creating pre_annotated_criterion rows expected 184 found {pac_ct}.")

        stmt = "select count(*) from pre_annotated_criterion a, pre_annotated_criterion_model b where a.id = b.pre_annotated_criterion_id and a.raw_criteria_id = 1"
        pacm_ct = db_session.execute(stmt).scalar_one()
        if pacm_ct != 208:
            errors.append(f"Error creating pre_annotated_criterion_model rows expected 208 found {pacm_ct}.")

    except Exception as ex:
        errors.append(f"SQL ERROR: create_raw_criteria_reload test: {ex}")

    assert not errors

@pytest.mark.asyncio
def test_create_raw_criteria_reupload_exact_dup(setup_database, client, connection):
    """
    This test simulates a re-upload of raw criteria from doccano for
    a study_version that currently exists in "NEW" status.

    """
    errors = []   
    fake_jwt = "1.2.3"
    test_raw_crit = "./tests/data/test_raw_criteria_exact_dup.zip"

    files = {'file': ('test_exact_dup.zip', open(test_raw_crit, 'rb'), 'application/zip')}
    resp = client.post("/raw-criteria", files=files, headers={"Authorization": f"bearer {fake_jwt}"})

    # load exact dup
    files = {'file': ('test_exact_dup.zip', open(test_raw_crit, 'rb'), 'application/zip')}
    resp = client.post("/raw-criteria", files=files, headers={"Authorization": f"bearer {fake_jwt}"})

    try:
        Session = sessionmaker(bind=connection)
        db_session = Session()
        """
        Based on input data, study TESTRAWCRIT_EXACT_DUP should have exactly one row
        in IN_PROCESS status.
        """
        stmt = select(StudyVersion).join(StudyVersion.study).join(StudyExternalId).where(
            StudyExternalId.ext_id == 'TESTRAWCRIT_EXACT_DUP').where(
                StudyVersion.status == StudyVersionStatus.NEW)
        svs = db_session.execute(stmt).unique()
        sv_rows_returned = len(svs.all())

        if sv_rows_returned != 1:
            errors.append(f"Raw-criteria exact dup re-upload test failed returned {sv_rows_returned} rows. Expecting one row.")

    except Exception as ex:
        errors.append(f"SQL ERROR: create_raw_criteria_reload test: {ex}")
    assert not errors