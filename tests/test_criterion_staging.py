import pytest

from gearbox import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from gearbox.models import CriterionStaging, Criterion
from gearbox.util.types import AdjudicationStatus


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
            "id": 28,
            "eligibility_criteria_id": 3,
            "input_id": None,
            "code": "karnofsky_score",
            "display_name": "display name",
            "description": "description",
            "create_date": "2024-07-22T12:26:36",
            "criterion_adjudication_status": "NEW",
            "echc_adjudication_status": "NEW",
            "ontology_code_id": None,
            "input_type_id": 3,
            "start_char": 2304,
            "end_char": 2340,
            "text": "TEST",
            "criterion_id": None,
            "last_updated_by_user_id": 1,
            "values": []
        }
    ]
)
def test_update_criterion_staging(setup_database, client, data, connection):

    fake_jwt = "1.2.3"
    resp = client.post(f"/update-criterion-staging", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")

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
    """
    Test endpoint that publishes a criterion_staging object to the criterion table
    """

    errors = []
    fake_jwt = "1.2.3"
    resp = client.post(f"/criterion-staging-publish-criterion", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    try:
        Session = sessionmaker(bind=connection)
        db_session = Session()
        stmt = select(CriterionStaging).where(CriterionStaging.id == data.get('criterion_staging_id'))
        row = db_session.execute(stmt).first()

        if not row:
            errors.append(f"ERROR: publish criterion_staging test failed to confirm new criterion_staging row found.")

        # validate status of newly published criterion staging
        elif row.CriterionStaging.criterion_adjudication_status != AdjudicationStatus.ACTIVE:
            errors.append(f"The published criterion (id={data.get('criterion_staging_id')} has the wrong status: {row.CriterionStaging.criterion_adjudication_status}")

        # validate row for new criterion was created
        stmt = select(Criterion).where(Criterion.id == row.CriterionStaging.criterion_id)
        row = db_session.execute(stmt).first()
        if not row:
            errors.append(f"Criterion not created during publish test for criterion_staging id {row.CriterionStaging.id}")
        
    except Exception as e:
        errors.append(f"SQL ERROR: publishing criterion_staging to criterion: {e}")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

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
    """
    Test endpoint that publishes a criterion_staging object to the criterion table
    with a criterion that has associated discrete values.
    """

    fake_jwt = "1.2.3"
    resp = client.post(f"/criterion-staging-publish-criterion", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
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
    """
    This tests endpoint that adds a row to the criterion_staging table directly.
    """

    fake_jwt = "1.2.3"
    resp = client.post(f"/criterion-staging", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")
