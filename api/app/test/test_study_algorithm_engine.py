import datetime
import json
import pytest

from app.main.model.study_algorithm_engine import StudyAlgorithmEngine
from app.main.controller.study_algorithm_engine_controller import StudyAlgorithmEngineInfo, AllStudyAlgorithmEnginesInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def study_algorithm_engineA():
    return StudyAlgorithmEngine(study_version_id = 2, algorithm_engine_pk = 1, algorithm_engine_id = 1)


@pytest.fixture(scope="module")
def study_algorithm_engineB():
    return StudyAlgorithmEngine(study_version_id = 3, algorithm_engine_pk = 1, algorithm_engine_id = 1)


def test_setup(study_algorithm_engineA, study_algorithm_engineB, app, session):
    session.add(study_algorithm_engineA)
    session.add(study_algorithm_engineB)


def test_scope(study_algorithm_engineA, study_algorithm_engineB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/study_algorithm_engine/info", method="GET"):        
        response = AllStudyAlgorithmEnginesInfo().get()
        table_data = response.json['body']
        assert study_algorithm_engineA.as_dict() in table_data
        assert study_algorithm_engineB.as_dict() in table_data


def test_study_algorithm_engine_info(study_algorithm_engineA, study_algorithm_engineB, app, session):
    for sag in [study_algorithm_engineA.as_dict(), study_algorithm_engineB.as_dict()]:
        with app.test_request_context("/study_algorithm_engine/{}-{}".format(sag['study_version_id'], sag['algorithm_engine_pk']), method="GET"):
            pid = "{}-{}".format(sag['study_version_id'], sag['algorithm_engine_pk'])
            response = StudyAlgorithmEngineInfo().get(pid)
            assert pid == "{}-{}".format(response['study_version_id'], response['algorithm_engine_pk'])


def test_all_study_algorithm_engines_info(study_algorithm_engineA, study_algorithm_engineB, app, session):
    with app.test_request_context("/study_algorithm_engine/info", method="GET"):        
        response = AllStudyAlgorithmEnginesInfo().get()
        assert response.status_code == 200
       
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert study_algorithm_engineA.as_dict() in table_data
        assert study_algorithm_engineB.as_dict() in table_data


def test_create_study_algorithm_engine(app, session):
    payload = {'study_version_id': 3, 'algorithm_engine_pk': 2, 'algorithm_engine_id': 1}
    with app.test_request_context("/study_algorithm_engine/create_study_algorithm_engine", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/study_algorithm_engine/info", method="GET"):        
        response = AllStudyAlgorithmEnginesInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            pid = "{}-{}".format(row['study_version_id'], row['algorithm_engine_pk'])
            if pid == '3-2':
                payload_seen = 1
        assert payload_seen == 1


def test_update_study_algorithm_engine(study_algorithm_engineA, study_algorithm_engineB, app, session):
    #basic update test
    study_algorithm_engineA_dict = study_algorithm_engineA.as_dict()
    pidA = "{}-{}".format(study_algorithm_engineA_dict['study_version_id'], study_algorithm_engineA_dict['algorithm_engine_pk'])
    payload = {'active': 1}
    
    with app.test_request_context("/study_algorithm_engine/update_study_algorithm_engine/{}".format(pidA), method="PUT", json=payload):
        response = Update().put(pidA)
        expected_response = study_algorithm_engineA_dict
        expected_response.update(payload)
        assert response == expected_response


def test_delete_study_algorithm_engine(study_algorithm_engineA, study_algorithm_engineB, app, session):
    study_algorithm_engineA_dict = study_algorithm_engineA.as_dict()
    pidA = "{}-{}".format(study_algorithm_engineA_dict['study_version_id'], study_algorithm_engineA_dict['algorithm_engine_pk'])

    with app.test_request_context("/study_algorithm_engine/delete_study_algorithm_engine/{}".format(pidA), method="DELETE"):
        response = Delete().delete(pidA)
        assert response == study_algorithm_engineA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/study_algorithm_engine/{}".format(pidA), method="GET"):
        try:
            response = StudyAlgorithmEngineInfo().get(pidA)
        except Exception as e:
            assert e.code == 404
