import json
import pytest

from app.main.model.criterion import Criterion
from app.main.controller.criterion_controller import CriterionInfo, AllCriterionsInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def criterionA():
    return Criterion(code = 'codeA', active = 0)


@pytest.fixture(scope="module")
def criterionB():
    return Criterion(code = 'codeB', active = 0)


def test_setup(criterionA, criterionB, app, session):
    session.add(criterionA)
    session.add(criterionB)


def test_scope(criterionA, criterionB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/criterion/info", method="GET"):        
        response = AllCriterionsInfo().get()
        table_data = response.json['body']
        assert criterionA.as_dict() in table_data
        assert criterionB.as_dict() in table_data


def test_criterion_info(criterionA, criterionB, app, session):
    for public_id in [criterionA.as_dict()['code'], criterionB.as_dict()['code']]:
        with app.test_request_context("/criterion/{}".format(public_id), method="GET"):
            response = CriterionInfo().get(public_id)
            assert public_id == response['code']


def test_all_criterions_info(criterionA, criterionB, app, session):
    with app.test_request_context("/criterion/info", method="GET"):        
        response = AllCriterionsInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert criterionA.as_dict() in table_data
        assert criterionB.as_dict() in table_data


def test_create_criterion(app, session):
    payload= {'code': 'thisCode', 'active': 0}
    with app.test_request_context("/criterion/create_criterion", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/criterion/info", method="GET"):        
        response = AllCriterionsInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['code'] == 'thisCode':
                payload_seen = 1
        assert payload_seen == 1


def test_update_criterion(criterionA, criterionB, app, session):
    #basic update test
    criterionA_dict = criterionA.as_dict()
    codeA = criterionA_dict['code']
    payload = {'display_name': 'this_display_name'} #update the name for criterionA
    with app.test_request_context("/criterion/update_criterion/{}".format(codeA), method="PUT", json=payload):
        response = Update().put(codeA)
        expected_response = criterionA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/criterion/{}".format(codeA), method="GET"):
        current_criterionA = CriterionInfo().get(codeA)
        
    #attempt re-use of public_id/code (expected 409)
    criterionB_dict = criterionB.as_dict()
    codeB = criterionB_dict['code']
    payload = {'code': codeB}
    with app.test_request_context("/criterion/update_criterion/{}".format(codeA), method="PUT", json=payload):
        try:
            response = Update().put(codeA)
        except Exception as e:
            assert e.code == 409    

def test_delete_criterion(criterionA, criterionB, app, session):
    criterionA_dict = criterionA.as_dict()
    codeA = criterionA_dict['code']

    with app.test_request_context("/criterion/delete_criterion/{}".format(codeA), method="DELETE"):
        response = Delete().delete(codeA)
        assert response == criterionA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/criterion/{}".format(codeA), method="GET"):
        try:
            response = CriterionInfo().get(codeA)
        except Exception as e:
            assert e.code == 404
