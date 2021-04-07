import datetime
import json
import pytest

from app.main.model.study_algorithm_engine import StudyAlgorithmEngine
from app.main.controller.study_algorithm_engine_controller import StudyAlgorithmEngineInfo, AllStudyAlgorithmEnginesInfo, Create, Delete


@pytest.fixture(scope="module")
def study_algorithm_engineA():
    return StudyAlgorithmEngine(study_version_id = 2, algorithm_engine_id = 1)


@pytest.fixture(scope="module")
def study_algorithm_engineB():
    return StudyAlgorithmEngine(study_version_id = 3, algorithm_engine_id = 1)


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
        payload = {'study_version_id': str(sag.get('study_version_id')), 'algorithm_engine_id': str(sag.get('algorithm_engine_id'))}
        with app.test_request_context("/study_algorithm_engine", method="GET", json=payload):
            response = StudyAlgorithmEngineInfo().get()
            r = json.loads(json.dumps(response), object_hook=lambda d: {k: int(v) if v and v.isdigit() else v for k, v in d.items()})
            assert sag == r


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
    payload = {'study_version_id': 4, 'algorithm_engine_id': 2}
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
            pid = "{}".format(row['study_version_id'])
            if pid == '4':
                payload_seen = 1
        assert payload_seen == 1


def test_delete_study_algorithm_engine(study_algorithm_engineA, study_algorithm_engineB, app, session):
    sagA_dict = study_algorithm_engineA.as_dict()
    payload = {'study_version_id': sagA_dict.get('study_version_id'), 'algorithm_engine_id': sagA_dict.get('algorithm_engine_id')}

    with app.test_request_context("/study_algorithm_engine/delete_study_algorithm_engine", method="DELETE", json=payload):
        response = Delete().delete()
        assert response == sagA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/study_algorithm_engine", method="GET", json=payload):
        try:
            response = StudyAlgorithmEngineInfo().get()
        except Exception as e:
            assert e.code == 404
