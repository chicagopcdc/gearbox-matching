import json
import pytest

from app.main.model.study_version import StudyVersion
from app.main.model.study import Study
from app.main.controller.study_version_controller import StudyVersionInfo, AllStudyVersionsInfo, Create, Update, Delete
from app.main.controller.study_controller import StudyInfo, AllStudiesInfo


@pytest.fixture(scope="module")
def study_versionA():
    return StudyVersion(id=2, study_id=1)

@pytest.fixture(scope="module")
def study_versionB():
    return StudyVersion(id=3, study_id=1)

#create a different study to attach the version to
@pytest.fixture(scope="module")
def studyA():
    return Study(name = 'studyA', code = 'codeA', active = 0)

@pytest.fixture(scope="module")
def studyB():
    return Study(name = 'studyB', code = 'codeB', active = 0)

def test_setup(study_versionA, study_versionB, studyA, studyB, app, session):
    session.add(study_versionA)
    session.add(study_versionB)
    session.add(studyA)
    session.add(studyB)

def get_study_id(this_study, app, session):
    code = this_study.as_dict()['code']
    with app.test_request_context("/study/{}".format(code), method="GET"):
        response = StudyInfo().get(code)
    return int(response['id'])

def get_study_version_id_max(app, session):
    with app.test_request_context("/study_version/info", method="GET"):        
        response = AllStudyVersionsInfo().get()
    r=response.json['body']
    id_max=0
    for item in r:
        if item['id']>id_max:
            id_max=item['id']
    return (id_max)

@pytest.fixture(scope="module")
def study_versionC(studyA, app, session):
    version_id = get_study_version_id_max(app,session)
    study_id = get_study_id(studyA, app, session)
    return StudyVersion(id=version_id+111, study_id=study_id, active=0)

def test_setup2(study_versionC, app, session):
    session.add(study_versionC)

def test_scope(study_versionA, study_versionB, study_versionC, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/study_version/info", method="GET"):        
        response = AllStudyVersionsInfo().get()
        table_data = response.json['body']
        assert study_versionA.as_dict() in table_data
        assert study_versionB.as_dict() in table_data
        assert study_versionC.as_dict() in table_data

def test_all_study_versions_info(study_versionA, study_versionB, study_versionC, app, session):
    with app.test_request_context("/study_version/info", method="GET"):        
        response = AllStudyVersionsInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert study_versionA.as_dict() in table_data
        assert study_versionB.as_dict() in table_data
        assert study_versionC.as_dict() in table_data

def test_create_study_version(studyA, app, session):
    version_id = get_study_version_id_max(app,session)
    study_id = get_study_id(studyA, app, session)
    payload= {'id':version_id+222, 'study_id':study_id, 'active':0}
    with app.test_request_context("/study_version/create_study_version", method="POST", json=payload):
        response, status_code = Create().post()
        assert status_code == 201

def test_scope_again(app, session):
    with app.test_request_context("/study_version/info", method="GET"):        
        response = AllStudyVersionsInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['id'] == 3:
                payload_seen = 1
        assert payload_seen == 1

def test_update_study_version(study_versionA, study_versionB, study_versionC, app, session):
    #basic update test
    study_versionC_dict = study_versionC.as_dict()
    activeC = study_versionC_dict['active']
    payload = {'active': 1-activeC} #update active for study_versionC
    idC=study_versionC_dict['id']
    with app.test_request_context("/study_version/update_study_version/{}".format(idC), method="PUT", json=payload):
        response = Update().put(idC)
        expected_response = study_versionC_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/study_version/{}".format(idC), method="GET"):
        current_study_versionA = StudyVersionInfo().get(idC)
        
    #attempt re-use of public_id/code (expected 409)
    study_versionB_dict = study_versionB.as_dict()
    idB = study_versionB_dict['id']
    payload = {'id': idB}
    with app.test_request_context("/study_version/update_study_version/{}".format(idC), method="PUT", json=payload):
        try:
            response = Update().put(idC)
        except Exception as e:
            assert e.code == 409    

def test_delete_study_version(study_versionA, study_versionB, app, session):
    study_versionA_dict = study_versionA.as_dict()
    idA = study_versionA_dict['id']

    with app.test_request_context("/study_version/delete_study_version/{}".format(idA), method="DELETE"):
        response = Delete().delete(idA)
        assert response == study_versionA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/study_version/{}".format(idA), method="GET"):
        try:
            response = StudyVersionInfo().get(idA)
        except Exception as e:
            assert e.code == 404
