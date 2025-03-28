import pytest
import random
import json

from sqlalchemy.orm import sessionmaker
from gearbox.models import Study
from deepdiff import DeepDiff

from .test_utils import is_aws_url

@pytest.mark.asyncio
def test_studies_compare(setup_database, client, connection):
    """
    Comments: This test builds the study document and compares vs studies.json 
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.post("/build-studies", headers={"Authorization": f"bearer {fake_jwt}"})
    test_studies = resp.json().get('studies')

    resp.raise_for_status()
    studydata_file = './tests/data/studies.json'

    """SERIALIZE STUDIES TO COMPARE AGAINST - UNCOMMENT TO WRITE NEW COMPARE DATA
    with open(studydata_file,'w') as comp_file:
        json.dump(test_studies, comp_file)
    """ 

    with open(studydata_file, 'r') as comp_file:
        study_compare = json.load(comp_file)

    studies = test_studies
    study_compare = study_compare

    diff = []
    # Diff all studies in the reponse that exist in the mock file
    for i in range(len(study_compare)):
        study_diff = DeepDiff(studies[i], study_compare[i], ignore_order=True)
        if (study_diff):
            diff.append(str(study_diff))
    
    assert not diff, "differences occurred: \n{}".format("\n".join(diff))            

@pytest.mark.asyncio
def test_get_studies(setup_database, client):
    """
    Comments: Test to validate aws url is returned from get endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    url = client.get("/studies", headers={"Authorization": f"bearer {fake_jwt}"})
    url_str =  url.content.decode('ascii').strip('\"')
    print(f"------> URL STR: {url_str}")

    assert is_aws_url(url_str)

@pytest.mark.asyncio
def test_get_study(setup_database, client):
    """
    Comments: Test to validate aws url is returned from get endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/study/1", headers={"Authorization": f"bearer {fake_jwt}"})
    assert str(resp.status_code).startswith("20")

@pytest.mark.asyncio
def test_get_study_not_exist(setup_database, client):
    """
    Comments: Test to validate aws url is returned from get endpoint
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/study/9999991", headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.json() == None

@pytest.mark.parametrize(
    "data", [ 
        {
            "name": "CREATE UPDATE TEST STUDY NAME",
            "code": "TEST STUDY CODE",
            "description": "test study description",
            "active": True
    }
    ]
)
@pytest.mark.asyncio
def test_create_study(setup_database, client, data, connection):
    """
    Comments: test create a new study and validates row created in db
    """
    fake_jwt = "1.2.3"
    test_study_code = 'TEST-STUDY-CODE'
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

    assert not errors, "errors occurred in test_create_study: \n{}".format("\n".join(errors))

@pytest.mark.asyncio
def test_build_studies(setup_database, client):
    errors = []
    fake_jwt = "1.2.3"
    resp = client.post("/build-studies", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    if not full_res.get('version'):
        errors.append("No version found in study json returned in test_build_studies")

    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_build_study (create): {resp.status_code} ")

    assert not errors, "errors occurred in test_build_studies: \n{}".format("\n".join(errors))



@pytest.mark.parametrize(
    "data", [ 
        {
            "name": "TEST BUILD STUDIES QUERY STUDY",
            "code": "TEST-BUILD-STUDIES-QUERY-CODE",
            "description": "test study description",
            "active": True
    }
    ]
)
@pytest.mark.asyncio
def test_build_studies_query(setup_database, client, data, connection):
    errors = []
    fake_jwt = "1.2.3"
    # insert test study
    resp = client.post("/study", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    resp = client.post("/build-studies", headers={"Authorization": f"bearer {fake_jwt}"})
    studies = resp.json().get('studies')

    # TEST-BUILD-STUDIES-QUERY-CODE should not be in the response because it has no associated
    # active study_version in the test data files
    if 'TEST-BUILD-STUDIES-QUERY-CODE' in [ study.get('code') for study in studies]:
        errors.append('ERROR: Study code TEST-BUILD-STUDIES-QUERY-CODE found in response - study has no associated study_version.')

    if not str(resp.status_code).startswith("20"):
        errors.append(f'ERROR: build-studies failed status: {resp.status_code} ') 
    
    #cleanup
    Session = sessionmaker(bind=connection)
    db_session = Session()
    d = db_session.query(Study).filter(Study.code=='TEST-BUILD-STUDIES-QUERY-CODE').delete()
    db_session.commit()
    db_session.close()



    assert not errors, "errors occurred in test_build_studies_query: \n{}".format("\n".join(errors))

@pytest.mark.asyncio
def test_update_study(setup_database, client, connection):
    """
    Comments: test to validate update study active to false
    """

    fake_jwt = "1.2.3"
    study_id=None
    errors = []
    data = {}
    data['active'] = False
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study_info = db_session.query(Study.id, Study.active).filter(Study.name=="CREATE UPDATE TEST STUDY NAME").first()
        si_dict = study_info._asdict()
        study_id = si_dict['id']
        study_active = si_dict['active']

        if not study_id: 
            errors.append("Update test error: Study to update not found.")
        if not study_active:
            errors.append("Update test error: Active already set to false.")

    except Exception as e:
            errors.append(f"Update test error: {e}.")

    resp = client.post(f"/update-study/{study_id}", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    try: 
        study_updated = db_session.query(Study).filter(Study.id==study_id).first()
        if study_updated.active != False:
            errors.append(f"Study (id): {study_id} update active to false failed")

    except Exception as e:
        errors.append(f"Test study unexpected exception: {str(e)}")

    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))
