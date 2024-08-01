import pytest
from sqlalchemy.orm import sessionmaker 
from gearbox.models import StudyVersion
from gearbox.util.types import StudyVersionStatus
from .test_utils import is_aws_url

@pytest.mark.parametrize(
    "data", [ 
        {
            "study_version": 
            {
                "study_id": 1,
                "status": "NEW"
            },
            "el_criteria_has_criterion": 
            {
                "echcs":
                    [
                        {
                            "criterion_id": 10,
                            "active": True,
                            "value_id": 91
                        },
                        {
                            "criterion_id": 10,
                            "active": True,
                            "value_id": 92
                        },
                        {
                            "criterion_id": 10,
                            "active": True,
                            "value_id": 93 
                        },
                        {
                            "criterion_id": 10,
                            "active": True,
                            "value_id": 34 
                        },
                        {
                            "criterion_id": 1,
                            "active": True,
                            "value_id": 89 
                        },
                    ]
            },
        }
    ]
)
def test_create_study_version_eligibility_criteria(setup_database, client, data, connection):
    fake_jwt = "1.2.3"
    resp = client.post("/study-version-eligibility-criteria", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    full_res = resp.json()

    errors = []
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study_id = data.get('study_version').get('study_id')
        study_version = db_session.query(StudyVersion).filter(StudyVersion.study_id==study_id).first()
        if not study_version: 
            errors.append(f"Study_version for study id: {study_id}not created")

        new_study_versions = db_session.query(StudyVersion).filter(StudyVersion.study_id==data.get('study_version').get('study_id')).filter(StudyVersion.status==StudyVersionStatus.ACTIVE).all()
        if len(new_study_versions) != 1:
            errors.append(f"Study id: {study_id} has {len(new_study_versions)} active study versions, should have exactly 1.")

    except Exception as e:
        errors.append(f"Test study_version unexpected exception: {str(e)}")
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study_version: {resp.status_code} ")

    print(f"******************** ERRORS: {errors}")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

@pytest.mark.asyncio
def test_update_study_version(setup_database, client, connection):
    fake_jwt = "1.2.3"
    errors = []
    data = {"status":StudyVersionStatus.IN_PROCESS.value, "id":2}
    study_version_id = 2

    resp = client.post(f"/update-study-version", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study_version_updated = db_session.query(StudyVersion).filter(StudyVersion.id==study_version_id).first()
        if study_version_updated.status != StudyVersionStatus.IN_PROCESS:
            errors.append(f"Study version (id): {study_version_id} update status to IN_PROCESS failed")

    except Exception as e:
        errors.append(f"Test study_version unexpected exception: {str(e)}")

    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study_version: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))
