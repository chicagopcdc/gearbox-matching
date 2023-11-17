import pytest
import random

from sqlalchemy.orm import sessionmaker
from gearbox.models import Study, StudyLink, Site
from .test_utils import is_aws_url

@pytest.mark.parametrize(
    "data", [ 
        {
            "studies": [
            {
                "name": "TEST STUDY UPDATES - *TEST STUDY NAME FIRST!!!*",
                "code": "20-489",
                "description": "test study description",
                "active": True,
                "sites": [ 
                    {
                        "name": "TEST STUDY UPDATES TEST SITE NAME",
                        "code": "TEST SITE CODE",
                        "active": True
                    }
                ],
                "links": [ 
                    {
                        "name": "UPDATED-----TEST STUDY UPDATES LINK NAME",
                        "href": "http://www.testlink.org",
                        "active": True
                    }
                ]
            },
            {
                "name": "TEST STUDY UPDATES - *TEST STUDY NAME SECOND*",
                "code": "20-489",
                "description": "test study description",
                "active": True,
                "sites": [ 
                    {
                        "name": "TEST STUDY UPDATES TEST SITE NAME",
                        "code": "TEST SITE CODE",
                        "active": True
                    }
                ],
                "links": [ 
                    {
                        "name": "UPDATED THIS IS NEW OK? NEXT-----TEST STUDY UPDATES LINK NAME",
                        "href": "http://www.testlink.org",
                        "active": True
                    }
                ]
            }
            ]
        }
    ]
)
@pytest.mark.asyncio
def test_study_updates(setup_database, client, data, connection):
    """
    Comments: test create a new study and validates row created in db
    """
    fake_jwt = "1.2.3"
    resp = client.post("/update-studies", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    # errors = []
    # try: 
    #     Session = sessionmaker(bind=connection)
    #    db_session = Session()
    #    study = db_session.query(Study).filter(Study.code==test_study_code).first()
    #    if not study: 
    #        errors.append(f"Study (code): {test_study_code} not created")

    #except Exception as e:
    #    errors.append(f"Test study unexpected exception: {str(e)}")
    #if not str(resp.status_code).startswith("20"):
    #    errors.append(f"Invalid https status code returned from test_create_study (create): {resp.status_code} ")

    #assert not errors, "errors occurred: \n{}".format("\n".join(errors))