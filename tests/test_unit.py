import pytest

from sqlalchemy.orm import sessionmaker 
from gearbox.models import Unit

def test_get_units(setup_database, client):
    """
    Comments: Test to validate aws url is returned from get endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/units", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    print(f"RESP: {full_res}")

    assert str(resp.status_code).startswith("20")

@pytest.mark.parametrize(
    "data", [ 
        {
            "name":  "create_new_unit_test_name",
        }
    ]
)
@pytest.mark.asyncio
def test_create_unit(setup_database, client, data, connection):
    """
    Comments: test create a new unit and validates row created in db
    """
    fake_jwt = "1.2.3"
    resp = client.post("/unit", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    errors = []
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        unit = db_session.query(Unit).filter(Unit.name==data['name']).first()
        if not unit: 
            errors.append(f"Unit for id: {data['unit_id']} not created")

    except Exception as e:
        errors.append(f"Test unit unexpected exception: {str(e)}")
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_unit: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

@pytest.mark.asyncio
def test_update_unit(setup_database, client, connection):
#    """
    # Comments: test to validate update unit name
#    """
    fake_jwt = "1.2.3"
    errors = []
    data = {"name":"NEW_UNIT_NAME"}
    unit_id = 2

    resp = client.post(f"/update-unit/{unit_id}", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        unit_updated = db_session.query(Unit).filter(Unit.id==unit_id).first()
        if unit_updated.name != "NEW_UNIT_NAME":
            errors.append(f"Unit (id): {unit_id} update failed")

    except Exception as e:
        errors.append(f"Test unit unexpected exception: {str(e)}")

    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_unit: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))