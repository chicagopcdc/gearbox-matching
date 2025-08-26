import pytest
import random

from sqlalchemy.orm import sessionmaker
from gearbox.models import Study, StudyLink, Site, StudyExternalId, SiteHasStudy, StudyVersion
from gearbox.util.types import StudyVersionStatus
from .test_utils import is_aws_url

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


@pytest.mark.parametrize(
    "data", [ 
        {
            "studies": [
            {
                "name": "TEST STUDY UPDATES - *TEST STUDY NAME FIRST!!!*",
                "code": "NEW_STUDY_CODE",
                "description": "test study description",
                "active": True,
                "sites": [ 
                    {
                        "name": "TEST STUDY UPDATES TEST SITE NAME",
                        "code": "TEST SITE CODE",
                    }
                ],
                "links": [ 
                    {
                        "name": "UPDATED-----TEST STUDY UPDATES LINK NAME",
                        "href": "http://www.testlink.org/",
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
                "name": "TEST STUDY UPDATES - *TEST STUDY NAME SECOND!!!*",
                "code": "NEW_STUDY_CODE_2",
                "description": "test study description",
                "active": True,
                "sites": [ 
                    {
                        "name": "TEST STUDY UPDATES TEST SITE NAME -> UPDATED",
                        "code": "TEST SITE CODE",
                        "country": "USA",
                        "status":"recruiting",
                        "city":"Chicago",
                        "state":"IL",
                        "zip":"60660"
                    }
                ],
                "links": [ 
                    {
                        "name": "UPDATED-----TEST STUDY UPDATES LINK NAME",
                        "href": "http://www.testlink.org-for-test",
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
            },
            {
                "name": "SECOND!!!*",
                "code": "NEW_STUDY_CODE_2",
                "description": "test study description",
                "active": True,
                "sites": [ 
                    {
                        "name": "TEST STUDY UPDATES TEST SITE NAME -> UPDATED",
                        "code": "TEST SITE CODE",
                        "country": "USA",
                        "status":"recruiting",
                        "city":"Chicago",
                        "state":"IL",
                        "zip":"60660"
                    }
                ],
                "links": [ 
                    {
                        "name": "UPDATED-----TEST STUDY UPDATES LINK NAME",
                        "href": "http://www.testlink.org-for-test",
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
            },
            {
                "name": "GVAX Plus Checkpoint Blockade in Neuroblastoma",
                "code": "19-680",
                "description": "This research clinical trial is studying the creation and administration of GVAX, an irradiated GM-CSF secreting, autologous neuroblastoma cell vaccine (GVAX) in combination with nivolumab and ipilimumab as a possible treatment for neuroblastoma.  The names of the study drugs involved in this study are:  GVAX Vaccine, an immunotherapy developed from surgically removed tumor tissue Nivolumab Ipilimumab",
                "active": True,
                "sites": [ 
                     {
                "name": "Dana Farber Cancer Institite"
            },
            {
                "name": "Boston Children's Hospital"
            }
                ],
                "links": [ 
                      {
                "name": "ClinicalTrials.gov",
                "href": "https://clinicaltrials.gov/ct2/show/NCT04239040"
            }
                ],
                "ext_ids": [
                      {
                "ext_id": "NCT04239040",
                "source": "NIH",
                "source_url": "https://clinicaltrials.gov"
            }
            ]
            }
            ],
            "source": "clinicaltrials.gov"
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

        links = db_session.query(StudyLink).all()
        link = db_session.query(StudyLink).filter(StudyLink.href.like(f'%{test_link}%')).first()
        if not link: 
            errors.append(f"Link (href): |{test_link}| not created")

        ext_id = db_session.query(StudyExternalId).filter(StudyExternalId.ext_id==test_ext_id).first()
        if not ext_id: 
            errors.append(f"Study external id (ext_id): {test_ext_id} not created")

        site_has_study = db_session.query(SiteHasStudy).filter(SiteHasStudy.study_id==study.id).first()
        if not site_has_study: 
            errors.append(f"Site has study(study_id): {study.id} not created")
        

        active_studies = db_session.query(Study).filter(Study.active==True).all()
        if not len(active_studies) == 3:
            errors.append(f"ERROR: should be 2 active studies, found: {len(active_studies)} active studies in study table.")

        active_links = db_session.query(StudyLink).filter(StudyLink.active==True).all()
        if not len(active_links) == 3:
            errors.append(f"ERROR: should be 2 active study links, found: {len(active_links)} active study links in study_links table.")

        active_study_sites = db_session.query(SiteHasStudy).filter(SiteHasStudy.active==True).all()
        if not len(active_study_sites) == 4:
            errors.append(f"ERROR: should be 2 active study sites, found: {len(active_study_sites)} active study sites in site_has_study table.")

        # confirm that study_version for inactive study was set to status = INACTIVE
        #inactive_study_version = db_session.query(StudyVersion).filter(StudyVersion.study_id==8).filter(StudyVersion.status=StudyVersionStatus.INACTIVE.value)
        inactive_study_version = db_session.query(StudyVersion).filter(StudyVersion.study_id==8).filter(StudyVersion.status==StudyVersionStatus.INACTIVE.value).all()
        if not len(inactive_study_version) == 1:
            errors.append(f"ERROR: study_version for study_id = 8 should be inactive")

    except Exception as e:
        errors.append(f"Test study unexpected exception: {str(e)}")
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study (create): {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))

@pytest.mark.parametrize(
    "data", [ 
        {
            "studies": [
            {
                "name": "TEST STUDY UPDATES - *TEST STUDY NAME FIRST!!!*",
                "code": "NEW_STUDY_CODE",
                "description": "test study description",
                "active": True,
                "sites": [ 
                    {
                        "name": "TEST STUDY UPDATES TEST SITE NAME",
                        "code": "TEST SITE CODE",
                    }
                ],
                "links": [ 
                    {
                        "name": "UPDATED-----TEST STUDY UPDATES LINK NAME",
                        "href": "http://www.testlink.org/",
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
            }
            ],
            "source": "unknown_source.gov"
        }
    ]
)
@pytest.mark.asyncio
def test_study_updates_unknown_source(setup_database, client, data, connection):
    """
    Comments: test create a new study and validates row created in db
    """
    fake_jwt = "1.2.3"
    resp = client.post("/update-studies", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == HTTP_500_INTERNAL_SERVER_ERROR

@pytest.mark.parametrize(
    "data", [ 
        {
            "studies": [
            {
                "name": "TEST STUDY UPDATES - *TEST STUDY NAME FIRST!!!*",
                "code": "NEW_STUDY_CODE",
                "description": "test study description",
                "active": True,
                "sites": [ 
                    {
                        "name": "TEST STUDY UPDATES TEST SITE NAME",
                        "code": "TEST SITE CODE",
                    }
                ],
                "links": [ 
                    {
                        "name": "UPDATED-----TEST STUDY UPDATES LINK NAME",
                        "href": "http://www.testlink.org/",
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
            }
            ]
        }
    ]
)
@pytest.mark.asyncio
def test_study_updates_missing_source(setup_database, client, data, connection):
    """
    Comments: test create a new study and validates row created in db
    """
    fake_jwt = "1.2.3"
    resp = client.post("/update-studies", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == HTTP_422_UNPROCESSABLE_ENTITY