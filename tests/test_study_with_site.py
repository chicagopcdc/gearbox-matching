import pytest
import random

from sqlalchemy.orm import sessionmaker
from gearbox.models import Study, StudyLink, Site
from .test_utils import is_aws_url

@pytest.mark.parametrize(
    "data", [ 
        {
            "name": "CREATE UPDATE TEST STUDY NAME",
            "code": "TEST STUDY CODE",
            "description": "test study description",
            "active": True,
            "sites": [ 
                {
                    "name": "CREATE UPDATE TEST SITE NAME",
                    "code": "TEST SITE CODE",
                    "active": True
                },
                {
                    "name": "CREATE UPDATE TEST SITE NAME 2",
                    "code": "TEST SITE CODE 2",
                    "active": True
                }
    ]
    }
    ]
)
@pytest.mark.asyncio
def test_create_study_with_sites(setup_database, client, data, connection):
    """
    Comments: test create a new study and validates row created in db
    """
    fake_jwt = "1.2.3"
    test_study_code = 'TESTCODE' + str(random.randint(0,9999))
    data['code'] = test_study_code
    resp = client.post("/study", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    errors = []
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study = db_session.query(Study).filter(Study.code==test_study_code).first()
        if not study: 
            errors.append(f"Study (code): {test_study_code} not created")

    except Exception as e:
        errors.append(f"Test study unexpected exception: {str(e)}")
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study (create): {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

@pytest.mark.parametrize(
    "data", [ 
        {
            "name": "CREATE UPDATE TEST STUDY NAME",
            "code": "TEST STUDY CODE",
            "description": "test study description",
            "active": True,
            "sites": [ 
                {
                    "name": "CREATE UPDATE TEST SITE NAME",
                    "code": "TEST SITE CODE",
                    "active": True
                }
            ],
            "links": [ 
                {
                    "name": "TEST LINK NAME",
                    "href": "http://www.testlink.org",
                    "active": True
                }
            ]
    }
    ]
)
@pytest.mark.asyncio
def test_create_study_with_sites_and_links(setup_database, client, data, connection):
    """
    Comments: test create a new study and validates row created in db
    """
    fake_jwt = "1.2.3"
    test_study_code = 'TESTCODE' + str(random.randint(0,9999))
    data['code'] = test_study_code
    resp = client.post("/study", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    study_link_name = data['links'][0]['name']
    site_name = data['sites'][0]['name']

    errors = []
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study = db_session.query(Study).filter(Study.code==test_study_code).first()
        if not study: 
            errors.append(f"Study (code): {test_study_code} not created")
        link = db_session.query(StudyLink).filter(StudyLink.name==study_link_name).first()
        if not link: 
            errors.append(f"Link (name): {study_link_name} not created")
        site = db_session.query(Site).filter(Site.name==site_name).first()
        if not site: 
            errors.append(f"Site (name): {site_name} not created")

    except Exception as e:
        errors.append(f"Test study unexpected exception: {str(e)}")
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study (create): {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))