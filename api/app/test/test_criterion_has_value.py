import json
import pytest

from app.main.model.criterion_has_value import CriterionHasValue
from app.main.controller.criterion_has_value_controller import CriterionHasValueInfo, AllCriterionHasValuesInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def criterion_has_valueA():
    return CriterionHasValue(value_id = 1, criterion_id = 1)


@pytest.fixture(scope="module")
def criterion_has_valueB():
    return CriterionHasValue(value_id = 2, criterion_id = 2)


def test_setup(criterion_has_valueA, criterion_has_valueB, app, session):
    session.add(criterion_has_valueA)
    session.add(criterion_has_valueB)


def test_scope(criterion_has_valueA, criterion_has_valueB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/criterion_has_value/info", method="GET"):        
        response = AllCriterionHasValuesInfo().get()
        table_data = response.json['body']
        assert criterion_has_valueA.as_dict() in table_data
        assert criterion_has_valueB.as_dict() in table_data


def test_criterion_has_value_info(criterion_has_valueA, criterion_has_valueB, app, session):
    for chv in [criterion_has_valueA.as_dict(), criterion_has_valueB.as_dict()]:
        with app.test_request_context("/criterion_has_value/{}-{}".format(chv['value_id'], chv['criterion_id']), method="GET"):
            pid = "{}-{}".format(chv['value_id'], chv['criterion_id'])
            response = CriterionHasValueInfo().get(pid)
            assert pid == "{}-{}".format(response['value_id'], response['criterion_id'])


def test_all_criterion_has_values_info(criterion_has_valueA, criterion_has_valueB, app, session):
    with app.test_request_context("/criterion_has_value/info", method="GET"):        
        response = AllCriterionHasValuesInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert criterion_has_valueA.as_dict() in table_data
        assert criterion_has_valueB.as_dict() in table_data


def test_create_criterion_has_value(app, session):
    payload= {'value_id': 1, 'criterion_id': 2}
    with app.test_request_context("/criterion_has_value/create_criterion_has_value", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/criterion_has_value/info", method="GET"):        
        response = AllCriterionHasValuesInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            pid = "{}-{}".format(row['value_id'], row['criterion_id'])
            if pid == '1-2':
                payload_seen = 1
        assert payload_seen == 1


def test_update_criterion_has_value(criterion_has_valueA, criterion_has_valueB, app, session):
    #basic update test
    criterion_has_valueA_dict = criterion_has_valueA.as_dict()
    pidA = "{}-{}".format(criterion_has_valueA_dict['value_id'], criterion_has_valueA_dict['criterion_id'])
    payload = {'value_id': 2, 'criterion_id': 1}
    with app.test_request_context("/criterion_has_value/update_criterion_has_value/{}".format(pidA), method="PUT", json=payload):
        response = Update().put(pidA)
        expected_response = criterion_has_valueA_dict
        expected_response.update(payload)
        assert response == expected_response
        

def test_delete_criterion_has_value(criterion_has_valueA, criterion_has_valueB, app, session):
    criterion_has_valueA_dict = criterion_has_valueA.as_dict()
    pidA = "{}-{}".format(criterion_has_valueA_dict['value_id'], criterion_has_valueA_dict['criterion_id'])

    with app.test_request_context("/criterion_has_value/delete_criterion_has_value/{}".format(pidA), method="DELETE"):
        response = Delete().delete(pidA)
        assert response == criterion_has_valueA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/criterion_has_value/{}".format(pidA), method="GET"):
        try:
            response = CriterionHasValueInfo().get(pidA)
        except Exception as e:
            assert e.code == 404
