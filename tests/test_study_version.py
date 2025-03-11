import pytest
from sqlalchemy.orm import sessionmaker 
from gearbox.models import StudyVersion
from gearbox.util.types import StudyVersionStatus
from .test_utils import is_aws_url


@pytest.mark.asyncio
def test_get_study_versions(setup_database, client):
    """
    Comments: Test to validate aws url is returned from get endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/study-versions", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

@pytest.mark.asyncio
def test_get_study_versions_for_adjudication(setup_database, client):
    """
    Comments: Test to validate aws url is returned from get endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/study-versions-adjudication", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    assert str(resp.status_code).startswith("20")

@pytest.mark.asyncio
def test_get_study_versions_by_status(setup_database, client):
    """
    Comments: Test to validate aws url is returned from get endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/study-versions/IN_PROCESS", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

@pytest.mark.parametrize(
    "data", [ 
        {
            "study_id": 3,
            "active": True,
            "status":"ACTIVE"
    }
    ]
)
def test_create_study_version(setup_database, client, data, connection):
    """
    Comments: test create a new study_version and validates row created in db
    """
    fake_jwt = "1.2.3"
    resp = client.post("/study-version", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    errors = []
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study_version = db_session.query(StudyVersion).filter(StudyVersion.study_id==data['study_id']).first()
        if not study_version: 
            errors.append(f"Study_version for study id: {data['study_id']} not created")

        #
        # Test: confirm that there exists only one active study version for the study id.
        #
        active_study_versions = db_session.query(StudyVersion).filter(StudyVersion.study_id==data['study_id']).filter(StudyVersion.status==StudyVersionStatus.ACTIVE).all()
        if len(active_study_versions) != 1:
            errors.append(f"Study id: {data['study_id']} has {len(active_study_versions)} active study versions, should have exactly 1.")

    except Exception as e:
        errors.append(f"Test study_version unexpected exception: {str(e)}")
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study_version: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

@pytest.mark.asyncio
def test_update_study_version(setup_database, client, connection):
#    """
    # Comments: test to validate update study_version active to false
#    """
    fake_jwt = "1.2.3"
    errors = []
    data = {"id":3, "status":"IN_PROCESS"}

    resp = client.post(f"/update-study-version", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study_version_updated = db_session.query(StudyVersion).filter(StudyVersion.id==data.get('id')).first()
        if study_version_updated.status!= StudyVersionStatus.IN_PROCESS:
            errors.append(f"Study version (id): {data.get('id')} update active to false failed")

    except Exception as e:
        errors.append(f"Test study_version unexpected exception: {str(e)}")

    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study_version: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

@pytest.mark.asyncio
def test_publish_study_version(setup_database, client, connection):
#    """
    # Comments: assert study version publish complete
#    """
    fake_jwt = "1.2.3"
    errors = []

    resp = client.post(f"/publish-study-version/21", headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

@pytest.mark.asyncio
def test_publish_study_version_incomplete_criterion_adjudication(setup_database, client, connection):
#    """
    # Comments: test fail for incomplete criterion adjudication
#    """
    fake_jwt = "1.2.3"
    errors = []

    resp = client.post(f"/publish-study-version/22", headers={"Authorization": f"bearer {fake_jwt}"})
    print(f"RESP: {resp.text}")
    assert 'staged criteria require final adjudication' in resp.text
    assert str(resp.status_code).startswith("50")

@pytest.mark.asyncio
def test_publish_study_version_incomplete_echc_adjudication(setup_database, client, connection):
#    """
    # Comments: test fail for incomplete el_criteria_has_criterion adjudication
#    """
    fake_jwt = "1.2.3"
    errors = []

    resp = client.post(f"/publish-study-version/23", headers={"Authorization": f"bearer {fake_jwt}"})
    print(f"RESP: {resp.text}")
    assert 'el_criteria_has_criterion adjudication is not finalized' in resp.text
    assert str(resp.status_code).startswith("50")

@pytest.mark.asyncio
def test_publish_study_version_existing_active_fail(setup_database, client, connection):
#    """
    # Comments: test fail for already exsiting active study version for study
#    """
    fake_jwt = "1.2.3"
    errors = []

    resp = client.post(f"/publish-study-version/1", headers={"Authorization": f"bearer {fake_jwt}"})
    print(f"RESP: {resp.text}")
    assert 'Existing ACTIVE study_versions found' in resp.text
    assert str(resp.status_code).startswith("50")

@pytest.mark.asyncio
def test_publish_study_version_contains_inactive_criterion(setup_database, client, connection):
#    """
    # Comments: test fail for study includes inactive criterion (that are not in match form)
#    """
    fake_jwt = "1.2.3"
    errors = []

    resp = client.post(f"/publish-study-version/24", headers={"Authorization": f"bearer {fake_jwt}"})
    print(f"RESP: {resp.text}")
    assert 'criterion ids are used in the study but are inactive' in resp.text
    assert str(resp.status_code).startswith("50")

@pytest.mark.asyncio
def test_publish_study_version_contains_invalid_echc_id(setup_database, client, connection):
#    """
    # Comments: test fail for study includes inactive criterion (that are not in match form)
#    """
    fake_jwt = "1.2.3"
    errors = []

    resp = client.post(f"/publish-study-version/25", headers={"Authorization": f"bearer {fake_jwt}"})
    print(f"RESP: {resp.text}")
    assert 'invalid criterion_staging.echc_value_ids' in resp.text
    assert str(resp.status_code).startswith("50")

@pytest.mark.asyncio
def test_publish_study_version_contains_invalid_criterion_id(setup_database, client, connection):
#    """
    # Comments: test fail for study includes inactive criterion (that are not in match form)
#    """
    fake_jwt = "1.2.3"
    errors = []

    resp = client.post(f"/publish-study-version/26", headers={"Authorization": f"bearer {fake_jwt}"})
    print(f"RESP: {resp.text}")
    assert 'invalid criterion_staging.criterion_value_ids' in resp.text
    assert str(resp.status_code).startswith("50")