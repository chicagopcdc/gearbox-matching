import json
import pytest

from app.main.model.value import Value
from app.main.controller.value_controller import ValueInfo, AllValuesInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def valueA():
    return Value(code = 'codeA')


@pytest.fixture(scope="module")
def valueB():
    return Value(code = 'codeB')


def test_setup(valueA, valueB, app, session):
    session.add(valueA)
    session.add(valueB)


def test_scope(valueA, valueB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/value/info", method="GET"):        
        response = AllValuesInfo().get()
        table_data = response.json['body']
        assert valueA.as_dict() in table_data
        assert valueB.as_dict() in table_data


def test_value_info(valueA, valueB, app, session):
    for public_id in [valueA.as_dict()['code'], valueB.as_dict()['code']]:
        with app.test_request_context("/value/{}".format(public_id), method="GET"):
            response = ValueInfo().get(public_id)
            assert public_id == response['code']


def test_all_values_info(valueA, valueB, app, session):
    with app.test_request_context("/value/info", method="GET"):        
        response = AllValuesInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert valueA.as_dict() in table_data
        assert valueB.as_dict() in table_data


def test_create_value(app, session):
    payload= {'code': 'thisCode'}
    with app.test_request_context("/value/create_value", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/value/info", method="GET"):        
        response = AllValuesInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['code'] == 'thisCode':
                payload_seen = 1
        assert payload_seen == 1


def test_update_value(valueA, valueB, app, session):
    #basic update test
    valueA_dict = valueA.as_dict()
    codeA = valueA_dict['code']
    payload = {'value_string': 'this_value_string'}
    with app.test_request_context("/value/update_value/{}".format(codeA), method="PUT", json=payload):
        response = Update().put(codeA)
        expected_response = valueA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/value/{}".format(codeA), method="GET"):
        current_valueA = ValueInfo().get(codeA)
        
    #attempt re-use of public_id/code (expected 409)
    valueB_dict = valueB.as_dict()
    codeB = valueB_dict['code']
    payload = {'code': codeB}
    with app.test_request_context("/value/update_value/{}".format(codeA), method="PUT", json=payload):
        try:
            response = Update().put(codeA)
        except Exception as e:
            assert e.code == 409    

def test_delete_value(valueA, valueB, app, session):
    valueA_dict = valueA.as_dict()
    codeA = valueA_dict['code']

    with app.test_request_context("/value/delete_value/{}".format(codeA), method="DELETE"):
        response = Delete().delete(codeA)
        assert response == valueA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/value/{}".format(codeA), method="GET"):
        try:
            response = ValueInfo().get(codeA)
        except Exception as e:
            assert e.code == 404
