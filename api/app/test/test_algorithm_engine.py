import json
import pytest

from app.main.model.algorithm_engine import AlgorithmEngine
from app.main.controller.algorithm_engine_controller import AlgorithmEngineInfo, AllAlgorithmEnginesInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def algorithm_engineA():
    return AlgorithmEngine(el_criteria_has_criterion_id = 1, parent_path = 'parentPathA')


@pytest.fixture(scope="module")
def algorithm_engineB():
    return AlgorithmEngine(el_criteria_has_criterion_id = 2, parent_path = 'parentPathB')


def test_setup(algorithm_engineA, algorithm_engineB, app, session):
    session.add(algorithm_engineA)
    session.add(algorithm_engineB)


def test_scope(algorithm_engineA, algorithm_engineB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/algorithm_engine/info", method="GET"):        
        response = AllAlgorithmEnginesInfo().get()
        table_data = response.json['body']
        assert algorithm_engineA.as_dict() in table_data
        assert algorithm_engineB.as_dict() in table_data


def test_algorithm_engine_info(algorithm_engineA, algorithm_engineB, app, session):
    for public_id in [algorithm_engineA.as_dict()['id'], algorithm_engineB.as_dict()['id']]:
        with app.test_request_context("/algorithm_engine/{}".format(public_id), method="GET"):
            response = AlgorithmEngineInfo().get(public_id)
            assert public_id == int(response['id'])


def test_all_algorithm_engines_info(algorithm_engineA, algorithm_engineB, app, session):
    with app.test_request_context("/algorithm_engine/info", method="GET"):        
        response = AllAlgorithmEnginesInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert algorithm_engineA.as_dict() in table_data
        assert algorithm_engineB.as_dict() in table_data


#def test_create_algorithm_engine(algorithm_engineA, algorithm_engineB, app, session):
def test_create_algorithm_engine(app, session):
    payload= {'el_criteria_has_criterion_id': 3}
    with app.test_request_context("/algorithm_engine/create_algorithm_engine", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/algorithm_engine/info", method="GET"):        
        response = AllAlgorithmEnginesInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['el_criteria_has_criterion_id'] == 3:
                payload_seen = 1
        assert payload_seen == 1


def test_update_algorithm_engine(algorithm_engineA, algorithm_engineB, app, session):
    #basic update test
    algorithm_engineA_dict = algorithm_engineA.as_dict()
    idA = algorithm_engineA_dict['id']
    payload = {'parent_path': algorithm_engineA_dict['parent_path']+'_updated'} #update the name for algorithm_engineA
    with app.test_request_context("/algorithm_engine/update_algorithm_engine/{}".format(idA), method="PUT", json=payload):
        response = Update().put(idA)
        expected_response = algorithm_engineA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/algorithm_engine/{}".format(idA), method="GET"):
        current_algorithm_engineA = AlgorithmEngineInfo().get(idA)
        
    #attempt re-use of public_id/code (expected 409)
    algorithm_engineB_dict = algorithm_engineB.as_dict()
    idB = algorithm_engineB_dict['id']
    payload = {'id': idB}
    with app.test_request_context("/algorithm_engine/update_algorithm_engine/{}".format(idA), method="PUT", json=payload):
        try:
            response = Update().put(idA)
        except Exception as e:
            assert e.code == 409


def test_delete_algorithm_engine(algorithm_engineA, app, session):
    algorithm_engineA_dict = algorithm_engineA.as_dict()
    idA = algorithm_engineA_dict['id']

    with app.test_request_context("/algorithm_engine/delete_algorithm_engine/{}".format(idA), method="DELETE"):
        response = Delete().delete(idA)
        assert response == algorithm_engineA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/algorithm_engine/{}".format(idA), method="GET"):
        try:
            response = AlgorithmEngineInfo().get(idA)
        except Exception as e:
            assert e.code == 404
