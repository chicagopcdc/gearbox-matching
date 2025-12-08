import pytest

from sqlalchemy.orm import sessionmaker 
from gearboxdatamodel.models import StudyLink

def test_get_study_links(setup_database, client):
    """
    Comments: Test to validate aws url is returned from get endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/study-links", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

@pytest.mark.parametrize(
    "data", [ 
        {
            "study_id": 1,
            "name":  "study link name",
            "href": "http://www.test-href.org",
            "active": True
    }
    ]
)
@pytest.mark.asyncio
def test_create_study_link(setup_database, client, data, connection):
    """
    Comments: test create a new study_link and validates row created in db
    """
    fake_jwt = "1.2.3"
    resp = client.post("/study-link", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    errors = []
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study_link = db_session.query(StudyLink).filter(StudyLink.study_id==data['study_id']).first()
        if not study_link: 
            errors.append(f"Study_link for study id: {data['study_id']} not created")

        #
        # Test: confirm that there exists only one active study link for the study id.
        #
        # active_study_links = db_session.query(Studylink).filter(Studylink.study_id==data['study_id']).filter(Studylink.active==True).all()
        # if len(active_study_links) != 1:
        #    errors.append(f"Study id: {data['study_id']} has {len(active_study_links)} active study links, should have exactly 1.")

    except Exception as e:
        errors.append(f"Test study_link unexpected exception: {str(e)}")
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study_link: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

@pytest.mark.asyncio
def test_update_study_link(setup_database, client, connection):
#    """
    # Comments: test to validate update study_link active to false
#    """
    fake_jwt = "1.2.3"
    errors = []
    data = {"active":False}
    study_link_id = 2

    resp = client.post(f"/update-study-link/{study_link_id}", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study_link_updated = db_session.query(StudyLink).filter(StudyLink.id==study_link_id).first()
        if study_link_updated.active != False:
            errors.append(f"Study link (id): {study_link_id} update active to false failed")

    except Exception as e:
        errors.append(f"Test study_link unexpected exception: {str(e)}")

    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study_link: {resp.status_code} ")
    assert not errors, "errors occurred: \n{}".format("\n".join(errors))