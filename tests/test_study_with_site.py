import pytest
import random
import json

from sqlalchemy.orm import sessionmaker, Session
from gearbox.models import Study
from deepdiff import DeepDiff

import respx

from gearbox import config
from .test_utils import is_aws_url

@respx.mock
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

@respx.mock
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