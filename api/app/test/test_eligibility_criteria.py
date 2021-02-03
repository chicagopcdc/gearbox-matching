import json
import pytest

from app.main.model.eligibility_criteria import EligibilityCriteria
from app.main.controller.eligibility_criteria_controller import EligibilityCriteriaInfo, AllEligibilityCriteriasInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def eligibility_criteriaA():
    return EligibilityCriteria(study_version_id=4, active = 0)


@pytest.fixture(scope="module")
def eligibility_criteriaB():
    return EligibilityCriteria(study_version_id=5, active = 0)


def test_setup(eligibility_criteriaA, eligibility_criteriaB, app, session):
    session.add(eligibility_criteriaA)
    session.add(eligibility_criteriaB)


def test_scope(eligibility_criteriaA, eligibility_criteriaB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/eligibility_criteria/info", method="GET"):        
        response = AllEligibilityCriteriasInfo().get()
        table_data = response.json['body']
        assert eligibility_criteriaA.as_dict() in table_data
        assert eligibility_criteriaB.as_dict() in table_data


def test_eligibility_criteria_info(eligibility_criteriaA, eligibility_criteriaB, app, session):
    for public_id in [eligibility_criteriaA.as_dict()['study_version_id'], eligibility_criteriaB.as_dict()['study_version_id']]:
        with app.test_request_context("/eligibility_criteria/{}".format(public_id), method="GET"):
            response = EligibilityCriteriaInfo().get(public_id)
            assert public_id == int(response['study_version_id'])


def test_all_eligibility_criterias_info(eligibility_criteriaA, eligibility_criteriaB, app, session):
    with app.test_request_context("/eligibility_criteria/info", method="GET"):        
        response = AllEligibilityCriteriasInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert eligibility_criteriaA.as_dict() in table_data
        assert eligibility_criteriaB.as_dict() in table_data


def test_create_eligibility_criteria(app, session):
    payload= {'study_version_id': 6, 'active': 1}
    with app.test_request_context("/eligibility_criteria/create_eligibility_criteria", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/eligibility_criteria/info", method="GET"):        
        response = AllEligibilityCriteriasInfo().get()
        table_data = response.json['body']
        print (table_data)
        payload_seen = 0
        for row in table_data:
            print (row)
            if row['active'] == 1:
                payload_seen = 1
        assert payload_seen == 1


def test_update_eligibility_criteria(eligibility_criteriaA, eligibility_criteriaB, app, session):
    #basic update test
    eligibility_criteriaA_dict = eligibility_criteriaA.as_dict()
    idA = eligibility_criteriaA_dict['study_version_id']
    payload = {'active': True} #make it active
    with app.test_request_context("/eligibility_criteria/update_eligibility_criteria/{}".format(idA), method="PUT", json=payload):
        response = Update().put(idA)
        expected_response = eligibility_criteriaA_dict
        expected_response.update(payload)
        assert response == expected_response

    with app.test_request_context("/eligibility_criteria/{}".format(idA), method="GET"):
        current_eligibility_criteriaA = EligibilityCriteriaInfo().get(idA)
        

def test_delete_eligibility_criteria(eligibility_criteriaA, eligibility_criteriaB, app, session):
    eligibility_criteriaA_dict = eligibility_criteriaA.as_dict()
    idA = eligibility_criteriaA_dict['study_version_id']
    
    with app.test_request_context("/eligibility_criteria/delete_eligibility_criteria/{}".format(idA), method="DELETE"):
        response = Delete().delete(idA)
        assert response == eligibility_criteriaA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/eligibility_criteria/{}".format(idA), method="GET"):
        try:
            response = EligibilityCriteriaInfo().get(idA)
        except Exception as e:
            assert e.code == 404
