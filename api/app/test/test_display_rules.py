import json
import pytest

from app.main.model.display_rules import DisplayRules
from app.main.controller.display_rules_controller import DisplayRulesInfo, AllDisplayRulessInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def display_rulesA():
    return DisplayRules(criterion_id=3, priority=3)


@pytest.fixture(scope="module")
def display_rulesB():
    return DisplayRules(criterion_id=4, priority=4)


def test_setup(display_rulesA, display_rulesB, app, session):
    session.add(display_rulesA)
    session.add(display_rulesB)


def test_scope(display_rulesA, display_rulesB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/display_rules/info", method="GET"):        
        response = AllDisplayRulessInfo().get()
        table_data = response.json['body']
        assert display_rulesA.as_dict() in table_data
        assert display_rulesB.as_dict() in table_data


def test_display_rules_info(display_rulesA, display_rulesB, app, session):
    for dr in [display_rulesA.as_dict(), display_rulesB.as_dict()]:
        with app.test_request_context("/display_rules/{}".format(dr['id']), method="GET"):
            pid = str(dr['id'])
            response = DisplayRulesInfo().get(dr['id'])
            assert pid == str(response['id'])


def test_all_display_ruless_info(display_rulesA, display_rulesB, app, session):
    with app.test_request_context("/display_rules/info", method="GET"):        
        response = AllDisplayRulessInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert display_rulesA.as_dict() in table_data
        assert display_rulesB.as_dict() in table_data


def test_create_display_rules(app, session):
    payload= {"criterion_id":5, "priority":5}
    with app.test_request_context("/display_rules/create_display_rules", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/display_rules/info", method="GET"):        
        response = AllDisplayRulessInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            criterion_id = str(row['id'])
            if str(criterion_id) == '5':
                payload_seen = 1
        assert payload_seen == 1


def test_update_display_rules(display_rulesA, display_rulesB, app, session):
    #basic update test
    display_rulesA_dict = display_rulesA.as_dict()
    pidA = str(display_rulesA_dict['id'])
    payload = {'priority': 10} #update the name for display_rulesA
    with app.test_request_context("/display_rules/update_display_rules/{}".format(pidA), method="PUT", json=payload):
        response = Update().put(pidA)
        expected_response = display_rulesA_dict
        expected_response.update(payload)
        assert response == expected_response
        

def test_delete_display_rules(display_rulesA, display_rulesB, app, session):
    display_rulesA_dict = display_rulesA.as_dict()
    pidA = str(display_rulesA_dict['id'])

    with app.test_request_context("/display_rules/delete_display_rules/{}".format(pidA), method="DELETE"):
        response = Delete().delete(pidA)
        assert response == display_rulesA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/display_rules/{}".format(pidA), method="GET"):
        try:
            response = DisplayRulesInfo().get(pidA)
        except Exception as e:
            assert e.code == 404
