import json
import pytest

from app.main.model.triggered_by import TriggeredBy
from app.main.controller.triggered_by_controller import TriggeredByInfo, AllTriggeredBysInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def triggered_byA():
    return TriggeredBy(display_rules_id=1, criterion_id=1, value_id=1, path = '1.2.3')


@pytest.fixture(scope="module")
def triggered_byB():
    return TriggeredBy(display_rules_id=2, criterion_id=2, value_id=2, path = '2.3.4')


def test_setup(triggered_byA, triggered_byB, app, session):
    session.add(triggered_byA)
    session.add(triggered_byB)


def test_scope(triggered_byA, triggered_byB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/triggered_by/info", method="GET"):        
        response = AllTriggeredBysInfo().get()
        table_data = response.json['body']
        assert triggered_byA.as_dict() in table_data
        assert triggered_byB.as_dict() in table_data


def test_triggered_by_info(triggered_byA, triggered_byB, app, session):
    for tb in [triggered_byA.as_dict(), triggered_byB.as_dict()]:
        with app.test_request_context("/triggered_by/{}".format(tb['id']), method="GET"):
            pid = str(tb['id'])
            response = TriggeredByInfo().get(tb['id'])
            assert pid == str(response['id'])


def test_all_triggered_bys_info(triggered_byA, triggered_byB, app, session):
    with app.test_request_context("/triggered_by/info", method="GET"):        
        response = AllTriggeredBysInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert triggered_byA.as_dict() in table_data
        assert triggered_byB.as_dict() in table_data


def test_create_triggered_by(app, session):
    payload= {"display_rules_id":2, "criterion_id":3, "value_id": 4, "path": "3.4.5"}
    with app.test_request_context("/triggered_by/create_triggered_by", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/triggered_by/info", method="GET"):        
        response = AllTriggeredBysInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            criterion_id = str(row['criterion_id'])
            value_id = str(row['value_id'])
            if str(criterion_id) == '3' and str(value_id) == '4':
                payload_seen = 1
        assert payload_seen == 1


def test_update_triggered_by(triggered_byA, triggered_byB, app, session):
    #basic update test
    triggered_byA_dict = triggered_byA.as_dict()
    pidA = str(triggered_byA_dict['id'])
    payload = {'path': "1.2"} #update the name for triggered_byA
    with app.test_request_context("/triggered_by/update_triggered_by/{}".format(pidA), method="PUT", json=payload):
        response = Update().put(pidA)
        expected_response = triggered_byA_dict
        expected_response.update(payload)
        assert response == expected_response
        

def test_delete_triggered_by(triggered_byA, triggered_byB, app, session):
    triggered_byA_dict = triggered_byA.as_dict()
    pidA = str(triggered_byA_dict['id'])

    with app.test_request_context("/triggered_by/delete_triggered_by/{}".format(pidA), method="DELETE"):
        response = Delete().delete(pidA)
        assert response == triggered_byA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/triggered_by/{}".format(pidA), method="GET"):
        try:
            response = TriggeredByInfo().get(pidA)
        except Exception as e:
            assert e.code == 404
