import pytest
from sqlalchemy.orm import sessionmaker 
from gearbox.models import EligibilityCriteriaInfo
from .test_utils import is_aws_url
from gearbox.util.types import EligibilityCriteriaInfoStatus


@pytest.mark.asyncio
def test_get_eligibility_criteria_infos(setup_database, client):
    """
    Comments: Test to validate aws url is returned from get endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/eligibility-criteria-infos", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

@pytest.mark.asyncio
def test_update_eligibility_criteria_info_status_inactive(setup_database, client, connection):
#    """
    # Comments: test to validate update eligibility_criteria_info active to false
#    """
    fake_jwt = "1.2.3"
    errors = []
    data = {"status":EligibilityCriteriaInfoStatus.INACTIVE.value}
    eligibility_criteria_info_id = 1

    resp = client.post(f"/update-eligibility-criteria-info/{eligibility_criteria_info_id}", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        eligibility_criteria_info_updated = db_session.query(EligibilityCriteriaInfo).filter(EligibilityCriteriaInfo.id==eligibility_criteria_info_id).first()
        if eligibility_criteria_info_updated.status.value != EligibilityCriteriaInfoStatus.INACTIVE.value:
            errors.append(f"Study version (id): {eligibility_criteria_info_id} update active to false failed")

    except Exception as e:
        errors.append(f"Test eligibility_criteria_info unexpected exception: {str(e)}")

    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_eligibility_criteria_info: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

@pytest.mark.asyncio
def test_update_eligibility_criteria_info_status_active(setup_database, client, connection):
#    """
    # Comments: test to validate update eligibility_criteria_info active to false
#    """
    fake_jwt = "1.2.3"
    errors = []
    data = {"status":EligibilityCriteriaInfoStatus.ACTIVE.value}
    eligibility_criteria_info_id = 15

    resp = client.post(f"/update-eligibility-criteria-info/{eligibility_criteria_info_id}", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        eligibility_criteria_info_updated = db_session.query(EligibilityCriteriaInfo).filter(EligibilityCriteriaInfo.id==eligibility_criteria_info_id).first()
        if eligibility_criteria_info_updated.status.value != EligibilityCriteriaInfoStatus.ACTIVE.value:
            errors.append(f"Study version (id): {eligibility_criteria_info_id} update active to false failed")

    except Exception as e:
        errors.append(f"Test eligibility_criteria_info unexpected exception: {str(e)}")

    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_eligibility_criteria_info: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))