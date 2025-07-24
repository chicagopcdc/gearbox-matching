import pytest
import random

from sqlalchemy.orm import sessionmaker, Session
from gearbox.models import Site

def test_get_sites(setup_database, client):
    """
    Comments: Test to validate aws url is returned from get endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/sites", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

def test_get_site(setup_database, client):
    """
    Comments: Test to validate aws url is returned from get endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/site/1", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

@pytest.mark.parametrize(
    "data", [ 
        {
            "name": "CREATE UPDATE TEST SITE NAME"
    }
    ]
)
def test_create_site(setup_database, client, data, connection):
    """
    Comments: test create a new site and validates row created in db
    """
    fake_jwt = "1.2.3"
    resp = client.post("/site", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    errors = []
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        test_site_name = "CREATE UPDATE TEST SITE NAME"
        site = db_session.query(Site).filter(Site.name==test_site_name).first()
        if not site: 
            errors.append(f"Site: {test_site_name} not created")

    except Exception as e:
        errors.append(f"Test site unexpected exception: {str(e)}")
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_site (create): {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

def test_update_site(setup_database, client, connection):
    """
    Comments: test to validate update site active to false
    """

    fake_jwt = "1.2.3"
    site_id=None
    errors = []
    data = {}

    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        site_info = db_session.query(Site.id).filter(Site.name=="CREATE UPDATE TEST SITE NAME").first()
        si_dict = site_info._asdict()
        site_id = si_dict['id']

        if not site_id: 
            errors.append("Update test error: Site to update not found.")

    except Exception as e:
            errors.append(f"Update test error: {e}.")

    resp = client.post(f"/update-site/{site_id}", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    try: 
        site_updated = db_session.query(Site).filter(Site.id==site_id).first()

    except Exception as e:
        errors.append(f"Test site unexpected exception: {str(e)}")

    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_site: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))
