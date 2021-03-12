import json
import pytest

from app.main.model.input_type_has_value import InputTypeHasValue
from app.main.controller.input_type_has_value_controller import InputTypeHasValueInfo, AllInputTypeHasValuesInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def input_type_has_valueA():
    return InputTypeHasValue(value_id=1, input_type_id=1)


@pytest.fixture(scope="module")
def input_type_has_valueB():
    return InputTypeHasValue(value_id=2, input_type_id=2)


def test_setup(input_type_has_valueA, input_type_has_valueB, app, session):
    session.add(input_type_has_valueA)
    session.add(input_type_has_valueB)


def test_scope(input_type_has_valueA, input_type_has_valueB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/input_type_has_value/info", method="GET"):        
        response = AllInputTypeHasValuesInfo().get()
        table_data = response.json['body']
        assert input_type_has_valueA.as_dict() in table_data
        assert input_type_has_valueB.as_dict() in table_data


def test_input_type_has_value_info(input_type_has_valueA, input_type_has_valueB, app, session):
    for ithv in [input_type_has_valueA.as_dict(), input_type_has_valueB.as_dict()]:
        with app.test_request_context("/input_type_has_value/{}".format(ithv['input_type_id']), method="GET"):
            pid = str(ithv['input_type_id'])
            response = InputTypeHasValueInfo().get(ithv['input_type_id'])
            assert pid == str(response['input_type_id'])


def test_all_input_type_has_values_info(input_type_has_valueA, input_type_has_valueB, app, session):
    with app.test_request_context("/input_type_has_value/info", method="GET"):        
        response = AllInputTypeHasValuesInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert input_type_has_valueA.as_dict() in table_data
        assert input_type_has_valueB.as_dict() in table_data


def test_create_input_type_has_value(app, session):
    payload= {"value_id":3, "input_type_id":3}
    with app.test_request_context("/input_type_has_value/create_input_type_has_value", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/input_type_has_value/info", method="GET"):        
        response = AllInputTypeHasValuesInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            input_type_id = str(row['input_type_id'])
            if str(input_type_id) == '3':
                payload_seen = 1
        assert payload_seen == 1


def test_update_input_type_has_value(input_type_has_valueA, input_type_has_valueB, app, session):
    #basic update test
    input_type_has_valueA_dict = input_type_has_valueA.as_dict()
    pidA = str(input_type_has_valueA_dict['input_type_id'])
    payload = {'value_id': 4} #update the name for input_type_has_valueA
    with app.test_request_context("/input_type_has_value/update_input_type_has_value/{}".format(pidA), method="PUT", json=payload):
        response = Update().put(pidA)
        expected_response = input_type_has_valueA_dict
        expected_response.update(payload)
        assert response == expected_response
        

def test_delete_input_type_has_value(input_type_has_valueA, input_type_has_valueB, app, session):
    input_type_has_valueA_dict = input_type_has_valueA.as_dict()
    pidA = str(input_type_has_valueA_dict['input_type_id'])

    with app.test_request_context("/input_type_has_value/delete_input_type_has_value/{}".format(pidA), method="DELETE"):
        response = Delete().delete(pidA)
        assert response == input_type_has_valueA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/input_type_has_value/{}".format(pidA), method="GET"):
        try:
            response = InputTypeHasValueInfo().get(pidA)
        except Exception as e:
            assert e.code == 404
