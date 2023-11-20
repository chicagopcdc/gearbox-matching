import pytest
import random

from sqlalchemy.orm import sessionmaker
from gearbox.models import Study, StudyLink, Site, StudyExternalId
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
                ],
                "ext_ids": [
                    {
                        "ext_id": "testexternalstudyid1",
                        "source": "test ext id source",
                        "source_url": "http://www.testsourceurl.gov",
                        "active": True

                    }

                ]
            },
            {
                "name": "TEST STUDY UPDATES - *TEST STUDY NAME FIRST!!!*",
                "code": "20-489",
                "description": "test study description",
                "active": True,
                "sites": [ 
                    {
                        "name": "TEST STUDY UPDATES TEST SITE NAME -> UPDATED",
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
                ],
            "ext_ids": [
                    {
                        "ext_id": "testexternalstudyid2",
                        "source": "test ext id source",
                        "source_url": "http://www.testsourceurl.gov",
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

    test_study_code = data.get('studies')[1].get('code')
    test_site_name = data.get('studies')[1].get('sites')[0].get('name')
    test_link = data.get('studies')[1].get('links')[0].get('href')
    test_ext_id = data.get('studies')[1].get('ext_ids')[0].get('ext_id')

    errors = []
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study = db_session.query(Study).filter(Study.code==test_study_code).first()
        if not study: 
            errors.append(f"Study (code): {test_study_code} not created")

        site = db_session.query(Site).filter(Site.name==test_site_name).first()
        if not site: 
            errors.append(f"Site (name): {test_site_name} not created")

        link = db_session.query(StudyLink).filter(StudyLink.href==test_link).first()
        if not link: 
            errors.append(f"Link (href): {test_link} not created")

        ext_id = db_session.query(StudyExternalId).filter(StudyExternalId.ext_id==test_ext_id).first()
        if not ext_id: 
            errors.append(f"Study external id (ext_id): {test_ext_id} not created")
        

    except Exception as e:
        errors.append(f"Test study unexpected exception: {str(e)}")
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study (create): {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))