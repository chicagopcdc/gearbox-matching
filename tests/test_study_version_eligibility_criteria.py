import pytest
from sqlalchemy.orm import sessionmaker 
from gearbox.models import StudyVersion
from .test_utils import is_aws_url

@pytest.mark.parametrize(
    "data", [ 
        {
            "study_version": 
            {
                "study_id": 1,
                "active": False
            },
            "eligibility_criteria": 
            {

            },
            "el_criteria_has_criterion": 
            {
                "echcs":
                    [
                        {
                            "criterion_id": 10,
                            "eligibility_criteria_id": 10,
                            "active": True,
                            "value_id": 91
                        },
                        {
                            "criterion_id": 10,
                            "eligibility_criteria_id": 10,
                            "active": True,
                            "value_id": 92
                        },
                        {
                            "criterion_id": 10,
                            "eligibility_criteria_id": 10,
                            "active": True,
                            "value_id": 93 
                        },
                        {
                            "criterion_id": 10,
                            "eligibility_criteria_id": 10,
                            "active": True,
                            "value_id": 34 
                        },
                        {
                            "criterion_id": 1,
                            "eligibility_criteria_id": 10,
                            "active": True,
                            "value_id": 89 
                        },
                    ]
            },
            "eligibility_criteria_info":
            {
                "active": False,
                #"study_version_id": 1,
                "study_algorithm_engine_id": 1,
                "eligibility_criteria_id": 1
            }
        }
    ]
)
def test_create_study_version_eligibility_criteria(setup_database, client, data, connection):
    fake_jwt = "1.2.3"
    resp = client.post("/study-version-eligibility-criteria", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    """
    errors = []
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study_version = db_session.query(StudyVersion).filter(StudyVersion.study_id==data['study_id']).first()
        if not study_version: 
            errors.append(f"Study_version for study id: {data['study_id']} not created")

        active_study_versions = db_session.query(StudyVersion).filter(StudyVersion.study_id==data['study_id']).filter(StudyVersion.active==True).all()
        if len(active_study_versions) != 1:
            errors.append(f"Study id: {data['study_id']} has {len(active_study_versions)} active study versions, should have exactly 1.")

    except Exception as e:
        errors.append(f"Test study_version unexpected exception: {str(e)}")
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study_version: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))
    """

"""
@pytest.mark.asyncio
def test_update_study_version(setup_database, client, connection):
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
"""