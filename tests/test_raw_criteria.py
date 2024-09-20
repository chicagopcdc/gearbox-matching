import pytest
import json
from sqlalchemy.orm import sessionmaker 
from gearbox.models import StudyVersion
from .test_utils import is_aws_url


@pytest.mark.asyncio
def test_get_raw_criteria_by_ec(setup_database, client):
    """
    Comments: Test to get raw_criteria by eligibility_criteria id
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/raw-criteria-ec/1", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

@pytest.mark.asyncio
def test_get_raw_criteria_by_id(setup_database, client):
    """
    Comments: Test to get raw_criteria by raw_criteria id
    """
    errors = []
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
def test_create_raw_criteria_existing(setup_database, client):
       
    fake_jwt = "1.2.3"
    test_raw_crit = "./tests/data/test_raw_criteria_existing.json"
    with open(test_raw_crit, 'r') as test_raw_crit_file:
        raw_crit_data = test_raw_crit_file.read()
    
    raw_crit_data = json.loads(raw_crit_data)
    resp = client.post("/raw-criteria", json=raw_crit_data, headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")