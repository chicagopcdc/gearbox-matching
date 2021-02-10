import json
import pytest

from app.main.model.el_criteria_has_criterion import ElCriteriaHasCriterion
from app.main.controller.el_criteria_has_criterion_controller import ElCriteriaHasCriterionInfo, AllElCriteriaHasCriterionsInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def el_criteria_has_criterionA():
    return ElCriteriaHasCriterion(criterion_id=2, eligibility_criteria_id=1, value_id=2)


@pytest.fixture(scope="module")
def el_criteria_has_criterionB():
    return ElCriteriaHasCriterion(criterion_id=3, eligibility_criteria_id=1, value_id=2)


def test_setup(el_criteria_has_criterionA, el_criteria_has_criterionB, app, session):
    session.add(el_criteria_has_criterionA)
    session.add(el_criteria_has_criterionB)


def test_scope(el_criteria_has_criterionA, el_criteria_has_criterionB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/el_criteria_has_criterion/info", method="GET"):        
        response = AllElCriteriaHasCriterionsInfo().get()
        table_data = response.json['body']
        assert el_criteria_has_criterionA.as_dict() in table_data
        assert el_criteria_has_criterionB.as_dict() in table_data


def test_el_criteria_has_criterion_info(el_criteria_has_criterionA, el_criteria_has_criterionB, app, session):
    for echc in [el_criteria_has_criterionA.as_dict(), el_criteria_has_criterionB.as_dict()]:
        with app.test_request_context("/el_criteria_has_criterion/{}-{}".format(echc['criterion_id'], echc['eligibility_criteria_id'], echc['value_id']), method="GET"):
            pid = "{}-{}-{}".format(echc['criterion_id'], echc['eligibility_criteria_id'], echc['value_id'])
            response = ElCriteriaHasCriterionInfo().get(pid)
            assert pid == "{}-{}-{}".format(response['criterion_id'], response['eligibility_criteria_id'], response['value_id'])


def test_all_el_criteria_has_criterions_info(el_criteria_has_criterionA, el_criteria_has_criterionB, app, session):
    with app.test_request_context("/el_criteria_has_criterion/info", method="GET"):        
        response = AllElCriteriaHasCriterionsInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert el_criteria_has_criterionA.as_dict() in table_data
        assert el_criteria_has_criterionB.as_dict() in table_data


def test_create_el_criteria_has_criterion(app, session):
    payload= {'criterion_id':2, 'eligibility_criteria_id':3, 'value_id':3}
    with app.test_request_context("/el_criteria_has_criterion/create_el_criteria_has_criterion", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/el_criteria_has_criterion/info", method="GET"):        
        response = AllElCriteriaHasCriterionsInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            pid = "{}-{}-{}".format(row['criterion_id'], row['eligibility_criteria_id'], row['value_id'])
            if pid == '2-3-3':
                payload_seen = 1
        assert payload_seen == 1


def test_update_el_criteria_has_criterion(el_criteria_has_criterionA, el_criteria_has_criterionB, app, session):
    #basic update test
    el_criteria_has_criterionA_dict = el_criteria_has_criterionA.as_dict()
    pidA = "{}-{}-{}".format(el_criteria_has_criterionA_dict['criterion_id'], el_criteria_has_criterionA_dict['eligibility_criteria_id'], el_criteria_has_criterionA_dict['value_id'])
    payload = {'active': 1} #update the name for el_criteria_has_criterionA
    with app.test_request_context("/el_criteria_has_criterion/update_el_criteria_has_criterion/{}".format(pidA), method="PUT", json=payload):
        response = Update().put(pidA)
        expected_response = el_criteria_has_criterionA_dict
        expected_response.update(payload)
        assert response == expected_response
        

def test_delete_el_criteria_has_criterion(el_criteria_has_criterionA, el_criteria_has_criterionB, app, session):
    el_criteria_has_criterionA_dict = el_criteria_has_criterionA.as_dict()
    pidA = "{}-{}-{}".format(el_criteria_has_criterionA_dict['criterion_id'], el_criteria_has_criterionA_dict['eligibility_criteria_id'], el_criteria_has_criterionA_dict['value_id'])

    with app.test_request_context("/el_criteria_has_criterion/delete_el_criteria_has_criterion/{}".format(pidA), method="DELETE"):
        response = Delete().delete(pidA)
        assert response == el_criteria_has_criterionA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/el_criteria_has_criterion/{}".format(pidA), method="GET"):
        try:
            response = ElCriteriaHasCriterionInfo().get(pidA)
        except Exception as e:
            assert e.code == 404
