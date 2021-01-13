import json
import pytest

from app.main.model.input_type import InputType
from app.main.controller.input_type_controller import InputTypeInfo, AllInputTypesInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def input_typeA():
    return InputType(type = 'typeA', name = 'nameA')


@pytest.fixture(scope="module")
def input_typeB():
    return InputType(type = 'typeB', name = 'nameB')


def test_setup(input_typeA, input_typeB, app, session):
    session.add(input_typeA)
    session.add(input_typeB)


def test_scope(input_typeA, input_typeB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/input_type/info", method="GET"):        
        response = AllInputTypesInfo().get()
        table_data = response.json['body']
        assert input_typeA.as_dict() in table_data
        assert input_typeB.as_dict() in table_data


def test_input_type_info(input_typeA, input_typeB, app, session):
    for public_id in [input_typeA.as_dict()['name'], input_typeB.as_dict()['name']]:
        with app.test_request_context("/input_type/{}".format(public_id), method="GET"):
            response = InputTypeInfo().get(public_id)
            assert public_id == response['name']


def test_all_input_types_info(input_typeA, input_typeB, app, session):
    with app.test_request_context("/input_type/info", method="GET"):        
        response = AllInputTypesInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert input_typeA.as_dict() in table_data
        assert input_typeB.as_dict() in table_data


def test_create_input_type(app, session):
    payload= {'name': 'thisName'}
    with app.test_request_context("/input_type/create_input_type", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/input_type/info", method="GET"):        
        response = AllInputTypesInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['name'] == 'thisName':
                payload_seen = 1
        assert payload_seen == 1


def test_update_input_type(input_typeA, input_typeB, app, session):
    #basic update test
    input_typeA_dict = input_typeA.as_dict()
    nameA = input_typeA_dict['name']
    payload = {'type': 'this_type'}
    with app.test_request_context("/input_type/update_input_type/{}".format(nameA), method="PUT", json=payload):
        response = Update().put(nameA)
        expected_response = input_typeA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/input_type/{}".format(nameA), method="GET"):
        current_input_typeA = InputTypeInfo().get(nameA)
        
    #attempt re-use of public_id/code (expected 409)
    input_typeB_dict = input_typeB.as_dict()
    nameB = input_typeB_dict['name']
    payload = {'name': nameB}
    with app.test_request_context("/input_type/update_input_type/{}".format(nameA), method="PUT", json=payload):
        try:
            response = Update().put(nameA)
        except Exception as e:
            assert e.code == 409    

def test_delete_input_type(input_typeA, input_typeB, app, session):
    input_typeA_dict = input_typeA.as_dict()
    nameA = input_typeA_dict['name']

    with app.test_request_context("/input_type/delete_input_type/{}".format(nameA), method="DELETE"):
        response = Delete().delete(nameA)
        assert response == input_typeA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/input_type/{}".format(nameA), method="GET"):
        try:
            response = InputTypeInfo().get(nameA)
        except Exception as e:
            assert e.code == 404
