import pytest

from gearbox import config

@pytest.mark.asyncio
def test_get_criterion_staging(setup_database, client):
    """
    Test get criterion-staging
    """
    
    fake_jwt = "1.2.3"
    resp = client.get("/criterion-staging/3", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    resp.raise_for_status()

@pytest.mark.asyncio
def test_get_criterion_staging_not_found(setup_database, client):
    
    fake_jwt = "1.2.3"
    resp = client.get("/criterion-staging/999", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("40")

@pytest.mark.parametrize(
    "data", [ 
        {
            "id": 1,
            "criterion_adjudication_status": "INACTIVE"
        }
    ]
)
def test_update_criterion_staging(setup_database, client, data, connection):

    fake_jwt = "1.2.3"
    resp = client.post(f"/update-criterion-staging", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")


"""
criterion_staging_id: Optional[int]
    code: Optional[str]
    display_name: Optional[str]
    description: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]
    ontology_code_id: Optional[int]
    input_type_id: int
"""
@pytest.mark.parametrize(
    "data", [ 
        {
            "criterion_staging_id": 28,
            "code": "karnofsky_score",
            "display_name": "test display name karnofsky score",
            "description": "test description",
            "input_type_id": 1
        }
    ]
)
def test_publish_criterion_staging(setup_database, client, data, connection):

    fake_jwt = "1.2.3"
    resp = client.post(f"/criterion-staging-publish", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")

@pytest.mark.parametrize(
    "data", [ 
        {
            "criterion_staging_id": 41,
            "code": "for-testing-purposes",
            "display_name": "test display name with values",
            "description": "test description with values",
            "input_type_id": 2,
            "values": [1,4,5]
        }
    ]
)
def test_publish_criterion_staging_with_values(setup_database, client, data, connection):

    fake_jwt = "1.2.3"
    resp = client.post(f"/criterion-staging-publish", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")

@pytest.mark.parametrize(
    "data", [ 
        {
            "criterion_staging_id": 99,
            "code": "age",
            "display_name": "What is the patient's current age (in years)?",
            "description": "test description with values",
            "input_type_id": 2,
            "values": [1,4,5]
        }
    ]
)
def test_publish_criterion_staging_with_values_duplicate(setup_database, client, data, connection):

    fake_jwt = "1.2.3"
    resp = client.post(f"/criterion-staging-publish", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("40")

@pytest.mark.parametrize(
    "data", [ 
        {
            "eligibility_criteria_id": 1,
            "input_id": 1,
            "code": "TEST-CODE",
            "display_name": "test display name",
            "description": "test description",
            "criterion_adjudication_status": "NEW",
            "echc_adjudication_status": "NEW",
            "input_type_id": 1,
            "start_char": 5,
            "end_char": 10,
            "text": "test text",
            "criterion_id": 8,
            "values": [155,156,15],
            "last_updated_by_user_id": 4
        }
    ]
)
def test_post_criterion_staging(setup_database, client, data, connection):

    fake_jwt = "1.2.3"
    resp = client.post(f"/criterion-staging", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")