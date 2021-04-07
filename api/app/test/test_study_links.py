import json
import pytest

from app.main.model.study_links import StudyLinks
from app.main.model.study import Study
from app.main.controller.study_links_controller import StudyLinksInfo, AllStudyLinkssInfo, Create, Update, Delete
from app.main.controller.study_controller import StudyInfo, AllStudiesInfo


@pytest.fixture(scope="module")
def study_linksA():
    return StudyLinks(study_id=1, name='name1', href='https://www.study1.org')

@pytest.fixture(scope="module")
def study_linksB():
    return StudyLinks(study_id=2, name='name2', href='https://www.study2.org')

def test_setup(study_linksA, study_linksB, app, session):
    session.add(study_linksA)
    session.add(study_linksB)

def test_scope(study_linksA, study_linksB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/study_links/info", method="GET"):        
        response = AllStudyLinkssInfo().get()
        table_data = response.json['body']
        assert study_linksA.as_dict() in table_data
        assert study_linksB.as_dict() in table_data


def test_study_links_info(study_linksA, study_linksB, app, session):
    for sl in [study_linksA.as_dict(), study_linksB.as_dict()]:
        with app.test_request_context("/study_links/{}".format(sl['id']), method="GET"):
            pid = str(sl['id'])
            response = StudyLinksInfo().get(sl['id'])
            assert pid == str(response['id'])


def test_all_study_links_info(study_linksA, study_linksB, app, session):
    with app.test_request_context("/study_links/info", method="GET"):        
        response = AllStudyLinkssInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert study_linksA.as_dict() in table_data
        assert study_linksB.as_dict() in table_data


def test_create_study_links(app, session):
    payload= {"study_id": 3}
    with app.test_request_context("/study_links/create_study_links", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/study_links/info", method="GET"):        
        response = AllStudyLinkssInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            study_id = str(row['study_id'])
            if str(study_id) == '3':
                payload_seen = 1
        assert payload_seen == 1


def test_update_study_links(study_linksA, study_linksB, app, session):
    #basic update test
    study_linksA_dict = study_linksA.as_dict()
    pidA = str(study_linksA_dict['id'])
    payload = {'study_id': 4} #update the name for study_linksA
    with app.test_request_context("/study_links/update_study_links/{}".format(pidA), method="PUT", json=payload):
        response = Update().put(pidA)
        expected_response = study_linksA_dict
        expected_response.update(payload)
        assert response == expected_response
        

def test_delete_study_links(study_linksA, study_linksB, app, session):
    study_linksA_dict = study_linksA.as_dict()
    pidA = str(study_linksA_dict['id'])

    with app.test_request_context("/study_links/delete_study_links/{}".format(pidA), method="DELETE"):
        response = Delete().delete(pidA)
        assert response == study_linksA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/study_links/{}".format(pidA), method="GET"):
        try:
            response = StudyLinksInfo().get(pidA)
        except Exception as e:
            assert e.code == 404
