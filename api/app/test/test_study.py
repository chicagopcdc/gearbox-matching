import json
import pytest

from app.main.model.study import Study
from app.main.controller.study_controller import StudyInfo, AllStudiesInfo, Create, Update, Delete 


#@pytest.fixture(scope="function")
@pytest.fixture(scope="module")
#@pytest.fixture(scope="session")
def studyA():
    return Study(name = 'studyA', code = 'codeA', active = 0)


#@pytest.fixture(scope="function")
@pytest.fixture(scope="module")
#@pytest.fixture(scope="session")
def studyB():
    return Study(name = 'studyB', code = 'codeB', active = 0)


def test_setup(studyA, studyB, app, session):
    session.add(studyA)
    session.add(studyB)
    session.commit()


def test_scope(studyA, studyB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/study/info", method="GET"):        
        response = AllStudiesInfo().get()
        table_data = response.json['body']
        assert studyA.as_dict() in table_data
        assert studyB.as_dict() in table_data


def test_study_info(studyA, studyB, app, session):
    for code in [studyA.as_dict()['code'], studyB.as_dict()['code']]:
        with app.test_request_context("/study/{}".format(code), method="GET"):
            response = StudyInfo().get(code)
            assert code == response['code']


def test_all_studies_info(studyA, studyB, app, session):
    with app.test_request_context("/study/info", method="GET"):        
        response = AllStudiesInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert studyA.as_dict() in table_data
        assert studyB.as_dict() in table_data


def test_create_study(studyA, studyB, app, session):
    payload= {'name': 'thisName', 'code': 'thisCode', 'active': 0}

    with app.test_request_context("/study/create_study", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/study/info", method="GET"):        
        response = AllStudiesInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['code'] == 'thisCode':
                payload_seen = 1
        assert payload_seen == 1


def test_update_study(studyA, studyB, app, session):
    #basic update test
    studyA_dict = studyA.as_dict()
    codeA = studyA_dict['code']
    payload = {'name': studyA_dict['name']+'_updated'} #update the name for studyA
    with app.test_request_context("/study/update_study/{}".format(codeA), method="PUT", json=payload):
        response = Update().put(codeA)
        expected_response = studyA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/study/{}".format(codeA), method="GET"):
        current_studyA = StudyInfo().get(codeA)
        
    #attempt re-use of public_id/code (expected 409)
    studyB_dict = studyB.as_dict()
    codeB = studyB_dict['code']
    payload = {'code': codeB}
    with app.test_request_context("/study/update_study/{}".format(codeA), method="PUT", json=payload):
        try:
            response = Update().put(codeA)
        except Exception as e:
            assert e.code == 409    

def test_delete_study(studyA, studyB, app, session):
    studyA_dict = studyA.as_dict()
    codeA = studyA_dict['code']

    with app.test_request_context("/study/delete_study/{}".format(codeA), method="DELETE"):
        response = Delete().delete(codeA)
        assert response == studyA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/study/{}".format(codeA), method="GET"):
        try:
            response = StudyInfo().get(codeA)
        except Exception as e:
            assert e.code == 404
