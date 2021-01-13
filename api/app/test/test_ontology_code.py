import json
import pytest

from app.main.model.ontology_code import OntologyCode
from app.main.controller.ontology_code_controller import OntologyCodeInfo, AllOntologyCodesInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def ontology_codeA():
    return OntologyCode(code = 'codeA')


@pytest.fixture(scope="module")
def ontology_codeB():
    return OntologyCode(code = 'codeB')


def test_setup(ontology_codeA, ontology_codeB, app, session):
    session.add(ontology_codeA)
    session.add(ontology_codeB)


def test_scope(ontology_codeA, ontology_codeB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/ontology_code/info", method="GET"):        
        response = AllOntologyCodesInfo().get()
        table_data = response.json['body']
        assert ontology_codeA.as_dict() in table_data
        assert ontology_codeB.as_dict() in table_data


def test_ontology_code_info(ontology_codeA, ontology_codeB, app, session):
    for public_id in [ontology_codeA.as_dict()['code'], ontology_codeB.as_dict()['code']]:
        with app.test_request_context("/ontology_code/{}".format(public_id), method="GET"):
            response = OntologyCodeInfo().get(public_id)
            assert public_id == response['code']


def test_all_ontology_codes_info(ontology_codeA, ontology_codeB, app, session):
    with app.test_request_context("/ontology_code/info", method="GET"):        
        response = AllOntologyCodesInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert ontology_codeA.as_dict() in table_data
        assert ontology_codeB.as_dict() in table_data


def test_create_ontology_code(app, session):
    payload= {'code': 'thisCode'}
    with app.test_request_context("/ontology_code/create_ontology_code", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/ontology_code/info", method="GET"):        
        response = AllOntologyCodesInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['code'] == 'thisCode':
                payload_seen = 1
        assert payload_seen == 1


def test_update_ontology_code(ontology_codeA, ontology_codeB, app, session):
    #basic update test
    ontology_codeA_dict = ontology_codeA.as_dict()
    codeA = ontology_codeA_dict['code']
    payload = {'name': 'this_name'}
    with app.test_request_context("/ontology_code/update_ontology_code/{}".format(codeA), method="PUT", json=payload):
        response = Update().put(codeA)
        expected_response = ontology_codeA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/ontology_code/{}".format(codeA), method="GET"):
        current_ontology_codeA = OntologyCodeInfo().get(codeA)
        
    #attempt re-use of public_id/code (expected 409)
    ontology_codeB_dict = ontology_codeB.as_dict()
    codeB = ontology_codeB_dict['code']
    payload = {'code': codeB}
    with app.test_request_context("/ontology_code/update_ontology_code/{}".format(codeA), method="PUT", json=payload):
        try:
            response = Update().put(codeA)
        except Exception as e:
            assert e.code == 409    

def test_delete_ontology_code(ontology_codeA, ontology_codeB, app, session):
    ontology_codeA_dict = ontology_codeA.as_dict()
    codeA = ontology_codeA_dict['code']

    with app.test_request_context("/ontology_code/delete_ontology_code/{}".format(codeA), method="DELETE"):
        response = Delete().delete(codeA)
        assert response == ontology_codeA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/ontology_code/{}".format(codeA), method="GET"):
        try:
            response = OntologyCodeInfo().get(codeA)
        except Exception as e:
            assert e.code == 404
