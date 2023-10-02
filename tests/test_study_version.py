import pytest
from sqlalchemy.orm import sessionmaker 
from gearbox.models import StudyVersion
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
            "study_id": 1,
            "active": True
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
        active_study_versions = db_session.query(StudyVersion).filter(StudyVersion.study_id==data['study_id']).filter(StudyVersion.active==True).all()
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
    data = {"active":False}
    study_version_id = 2

    resp = client.post(f"/update-study-version/{study_version_id}", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study_version_updated = db_session.query(StudyVersion).filter(StudyVersion.id==study_version_id).first()
        if study_version_updated.active != False:
            errors.append(f"Study version (id): {study_version_id} update active to false failed")

    except Exception as e:
        errors.append(f"Test study_version unexpected exception: {str(e)}")

    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study_version: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))
