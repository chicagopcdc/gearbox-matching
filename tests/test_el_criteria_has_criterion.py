import pytest
import random
from starlette.config import environ
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

@pytest.mark.parametrize(
    "data", [ 
        { "echcs":
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
            "value_id": 95 
                },
                {
            "criterion_id": 1,
            "eligibility_criteria_id": 10,
            "active": True,
            "value_id": 96 
                },
            ]
        }
    ]
)
@pytest.mark.asyncio
def test_create_el_criteria_has_criterion(setup_database, client, data):
    """
    Test create el_criteria_has_criterion
    """
    print(f"IN TEST DATA TYPE: {type(data)}")
    print(f"IN TEST DATA TYPE: {data}")
    fake_jwt = "1.2.3"
    resp = client.post("/el-criteria-has-criterion", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")

@pytest.mark.parametrize(
    "data", [ 
        { "echcs":
            [
                {
            "criterion_id": 1,
            "eligibility_criteria_id": 1,
            "active": True,
            "value_id": 22 
                },
                {
            "criterion_id": 1,
            "eligibility_criteria_id": 1,
            "active": True,
            "value_id": 22 
                },
            ]
        }
    ]
)
@pytest.mark.asyncio
def test_create_duplicate_el_criteria_has_criterion(setup_database, client, data):
    """
    Test create el_criteria_has_criterion
    """
    fake_jwt = "1.2.3"
    resp = client.post("/el-criteria-has-criterion", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("409")

@pytest.mark.parametrize(
    "data", [ 
        { "echcs":
            [
                {
            "criterion_id": 1,
            "eligibility_criteria_id": 1,
            "active": True,
            "value_id": 22 
                },
                {
            "criterion_id": 8,
            "eligibility_criteria_id": 2,
            "active": True,
            "value_id": 59 
                },
            ]
        }
    ]
)
@pytest.mark.asyncio
def test_create_duplicate_db_el_criteria_has_criterion(setup_database, client, data):
    """
    Test create el_criteria_has_criterion
    """
    fake_jwt = "1.2.3"
    resp = client.post("/el-criteria-has-criterion", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("409")

@pytest.mark.asyncio
def test_get_el_criteria_has_criterions(setup_database, client):
    """
    Test that the /el_criteria_has_criterions endpoint returns a 200 and the id of the latest saved obj
    """
    fake_jwt = "1.2.3"
    resp = client.get("/el-criteria-has-criterions", headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == 200

@pytest.mark.asyncio
def test_get_el_criteria_has_criterion(setup_database, client):
    """
    Test that the /el_criteria_has_criterions endpoint returns a 200 and the id of the latest saved obj
    """
    fake_jwt = "1.2.3"
    resp = client.get("/el-criteria-has-criterion/1", headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == 200


# TO DO: create test for violating unique constraint