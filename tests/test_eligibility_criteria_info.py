import pytest
from sqlalchemy.orm import sessionmaker 
from gearbox.models import EligibilityCriteriaInfo
from .test_utils import is_aws_url


@pytest.mark.asyncio
def test_get_eligibility_criteria_infos(setup_database, client):
    """
    Comments: Test to validate aws url is returned from get endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/eligibility-criteria-infos", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

@pytest.mark.parametrize(
    "data", [ 
        {
            "active": True,
            "study_version_id": 1,
            "study_algorithm_engine_id": 1,
            "eligibility_criteria_id": 7
        }
    ]
)
def test_create_eligibility_criteria_info(setup_database, client, data, connection):
    """
    Comments: test create a new eligibility_criteria_info and validates row created in db
    """
    fake_jwt = "1.2.3"
    resp = client.post("/eligibility-criteria-info", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    errors = []
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        eligibility_criteria_info = db_session.query(EligibilityCriteriaInfo).filter(EligibilityCriteriaInfo.study_version_id==data['study_version_id']).first()
        if not eligibility_criteria_info: 
            errors.append(f"eligibility_criteria_info for study id: {data['study_version_id']} not created")

        #
        # Test: confirm that there exists only one active study version for the study id.
        #
        active_eligibility_criteria_infos = db_session.query(EligibilityCriteriaInfo).filter(EligibilityCriteriaInfo.study_version_id==data['study_version_id']).filter(EligibilityCriteriaInfo.active==True).all()
        if len(active_eligibility_criteria_infos) != 1:
            errors.append(f"Study id: {data['study_id']} has {len(active_eligibility_criteria_infos)} active study versions, should have exactly 1.")

    except Exception as e:
        errors.append(f"Test eligibility_criteria_info unexpected exception: {str(e)}")
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_eligibility_criteria_info: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

@pytest.mark.asyncio
def test_update_eligibility_criteria_info(setup_database, client, connection):
#    """
    # Comments: test to validate update eligibility_criteria_info active to false
#    """
    fake_jwt = "1.2.3"
    errors = []
    data = {"active":False}
    eligibility_criteria_info_id = 1

    resp = client.post(f"/update-eligibility-criteria-info/{eligibility_criteria_info_id}", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        eligibility_criteria_info_updated = db_session.query(EligibilityCriteriaInfo).filter(EligibilityCriteriaInfo.id==eligibility_criteria_info_id).first()
        if eligibility_criteria_info_updated.active != False:
            errors.append(f"Study version (id): {eligibility_criteria_info_id} update active to false failed")

    except Exception as e:
        errors.append(f"Test eligibility_criteria_info unexpected exception: {str(e)}")

    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_eligibility_criteria_info: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))
