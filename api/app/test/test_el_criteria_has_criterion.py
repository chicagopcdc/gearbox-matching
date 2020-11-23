import json
import pytest

from app.main.model.el_criteria_has_criterion import ElCriteriaHasCriterion
from app.main.controller.el_criteria_has_criterion_controller import ElCriteriaHasCriterionInfo, AllElCriteriaHasCriterionsInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def el_criteria_has_criterionA():
    return ElCriteriaHasCriterion(criterion_id=1, eligibility_criteria_id=1, code = 'codeA', display_name = 'display_nameA')


@pytest.fixture(scope="module")
def el_criteria_has_criterionB():
    return ElCriteriaHasCriterion(criterion_id=2, eligibility_criteria_id=2, code = 'codeB')


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
    for public_id in [el_criteria_has_criterionA.as_dict()['code'], el_criteria_has_criterionB.as_dict()['code']]:
        with app.test_request_context("/el_criteria_has_criterion/{}".format(public_id), method="GET"):
            response = ElCriteriaHasCriterionInfo().get(public_id)
            assert public_id == response['code']


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
    payload= {'criterion_id':2, 'eligibility_criteria_id':1, 'display_name': 'thisName', 'code': 'thisCode', 'active': 0}
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
            if row['code'] == 'thisCode':
                payload_seen = 1
        assert payload_seen == 1


def test_update_el_criteria_has_criterion(el_criteria_has_criterionA, el_criteria_has_criterionB, app, session):
    #basic update test
    el_criteria_has_criterionA_dict = el_criteria_has_criterionA.as_dict()
    codeA = el_criteria_has_criterionA_dict['code']
    payload = {'display_name': el_criteria_has_criterionA_dict['display_name']+'_update'} #update the name for el_criteria_has_criterionA
    with app.test_request_context("/el_criteria_has_criterion/update_el_criteria_has_criterion/{}".format(codeA), method="PUT", json=payload):
        response = Update().put(codeA)
        expected_response = el_criteria_has_criterionA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/el_criteria_has_criterion/{}".format(codeA), method="GET"):
        current_el_criteria_has_criterionA = ElCriteriaHasCriterionInfo().get(codeA)
        
    #attempt re-use of public_id/code (expected 409)
    el_criteria_has_criterionB_dict = el_criteria_has_criterionB.as_dict()
    codeB = el_criteria_has_criterionB_dict['code']
    payload = {'code': codeB}
    with app.test_request_context("/el_criteria_has_criterion/update_el_criteria_has_criterion/{}".format(codeA), method="PUT", json=payload):
        try:
            response = Update().put(codeA)
        except Exception as e:
            assert e.code == 409    

def test_delete_el_criteria_has_criterion(el_criteria_has_criterionA, el_criteria_has_criterionB, app, session):
    el_criteria_has_criterionA_dict = el_criteria_has_criterionA.as_dict()
    codeA = el_criteria_has_criterionA_dict['code']

    with app.test_request_context("/el_criteria_has_criterion/delete_el_criteria_has_criterion/{}".format(codeA), method="DELETE"):
        response = Delete().delete(codeA)
        assert response == el_criteria_has_criterionA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/el_criteria_has_criterion/{}".format(codeA), method="GET"):
        try:
            response = ElCriteriaHasCriterionInfo().get(codeA)
        except Exception as e:
            assert e.code == 404
