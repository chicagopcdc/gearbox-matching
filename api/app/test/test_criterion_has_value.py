import json
import pytest

from app.main.model.criterion_has_value import CriterionHasValue
from app.main.controller.criterion_has_value_controller import CriterionHasValueInfo, AllCriterionHasValuesInfo, Create, Delete


@pytest.fixture(scope="module")
def criterion_has_valueA():
    return CriterionHasValue(value_id=1, criterion_id=1)


@pytest.fixture(scope="module")
def criterion_has_valueB():
    return CriterionHasValue(value_id=2, criterion_id=2)


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
        payload = {'criterion_id': chv.get('criterion_id'), 'value_id': chv.get('value_id')}
        with app.test_request_context("/criterion_has_value", method="GET", json=payload):
            response = CriterionHasValueInfo().get()
            r = json.loads(json.dumps(response), object_hook=lambda d: {k: int(v) if v and v.isdigit() else v for k, v in d.items()})
            assert chv == r


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
    payload= {"value_id":3, "criterion_id":3}
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
            input_type_id = str(row['criterion_id'])
            if str(input_type_id) == '3':
                payload_seen = 1
        assert payload_seen == 1


def test_delete_criterion_has_value(criterion_has_valueA, criterion_has_valueB, app, session):
    chvA_dict = criterion_has_valueA.as_dict()
    payload = {'criterion_id': chvA_dict.get('criterion_id'), 'value_id': chvA_dict.get('value_id')}
    with app.test_request_context("/criterion_has_value/delete_criterion_has_value", method="DELETE", json=payload):
        response = Delete().delete()
        assert response == chvA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/criterion_has_value", method="GET", json=payload):
        try:
            response = CriterionHasValueInfo().get()
        except Exception as e:
            assert e.code == 404
