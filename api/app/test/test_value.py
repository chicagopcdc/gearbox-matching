import json
import pytest

from app.main.model.value import Value
from app.main.controller.value_controller import ValueInfo, AllValuesInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def valueA():
    return Value(code = 'codeA', value_string='valueA')


@pytest.fixture(scope="module")
def valueB():
    return Value(code = 'codeB', value_string='valueB')


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
    for val in [valueA.as_dict(), valueB.as_dict()]:
        with app.test_request_context("/value/{}".format(val['id']), method="GET"):
            pid = "{}".format(val['id'])
            response = ValueInfo().get(pid)
            assert pid == "{}".format(response['id'])


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
    payload= {'code': 'thisCode', 'value_string': 'this_val_str'}
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
            pid = "{}*{}".format(row['code'], row['value_string'])
            if pid == 'thisCode*this_val_str':
                payload_seen = 1
        assert payload_seen == 1


def test_update_value(valueA, valueB, app, session):
    #basic update test
    valueA_dict = valueA.as_dict()
    pidA = "{}".format(valueA_dict['id'])
    payload = {'value_string': 'this_other_value_str'}
    with app.test_request_context("/value/update_value/{}".format(pidA), method="PUT", json=payload):
        response = Update().put(pidA)
        expected_response = valueA_dict
        expected_response.update(payload)
        assert response == expected_response


def test_delete_value(valueA, valueB, app, session):
    valueA_dict = valueA.as_dict()
    pidA = "{}".format(valueA_dict['id'])

    with app.test_request_context("/value/delete_value/{}".format(pidA), method="DELETE"):
        response = Delete().delete(pidA)
        assert response == valueA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/value/{}".format(pidA), method="GET"):
        try:
            response = ValueInfo().get(pidA)
        except Exception as e:
            assert e.code == 404
