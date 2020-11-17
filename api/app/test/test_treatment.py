import json
import pytest

from app.main.model.treatment import Treatment
from app.main.controller.treatment_controller import TreatmentInfo, AllTreatmentsInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def treatmentA():
    return Treatment(level_code = 'level_codeA', description = 'descriptionA', active = 0)


@pytest.fixture(scope="module")
def treatmentB():
    return Treatment(level_code = 'level_codeB', description = 'descriptionB', active = 0)


def test_setup(treatmentA, treatmentB, app, session):
    session.add(treatmentA)
    session.add(treatmentB)


def test_scope(treatmentA, treatmentB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/treatment/info", method="GET"):        
        response = AllTreatmentsInfo().get()
        table_data = response.json['body']
        assert treatmentA.as_dict() in table_data
        assert treatmentB.as_dict() in table_data


def test_treatment_info(treatmentA, treatmentB, app, session):
    for public_id in [treatmentA.as_dict()['level_code'], treatmentB.as_dict()['level_code']]:
        with app.test_request_context("/treatment/{}".format(public_id), method="GET"):
            response = TreatmentInfo().get(public_id)
            assert public_id == response['level_code']


def test_all_treatments_info(treatmentA, treatmentB, app, session):
    with app.test_request_context("/treatment/info", method="GET"):        
        response = AllTreatmentsInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert treatmentA.as_dict() in table_data
        assert treatmentB.as_dict() in table_data


def test_create_treatment(app, session):
    payload= {'level_code': 'this_level_code', 'active': 0}
    with app.test_request_context("/treatment/create_treatment", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/treatment/info", method="GET"):        
        response = AllTreatmentsInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['level_code'] == 'this_level_code':
                payload_seen = 1
        assert payload_seen == 1


def test_update_treatment(treatmentA, treatmentB, app, session):
    #basic update test
    treatmentA_dict = treatmentA.as_dict()
    codeA = treatmentA_dict['level_code']
    payload = {'description': treatmentA_dict['description']+'_updated'} #update the name for treatmentA
    with app.test_request_context("/treatment/update_treatment/{}".format(codeA), method="PUT", json=payload):
        response = Update().put(codeA)
        expected_response = treatmentA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/treatment/{}".format(codeA), method="GET"):
        current_treatmentA = TreatmentInfo().get(codeA)
        
    #attempt re-use of public_id/code (expected 409)
    treatmentB_dict = treatmentB.as_dict()
    codeB = treatmentB_dict['level_code']
    payload = {'level_code': codeB}
    with app.test_request_context("/treatment/update_treatment/{}".format(codeA), method="PUT", json=payload):
        try:
            response = Update().put(codeA)
        except Exception as e:
            assert e.code == 409    

def test_delete_treatment(treatmentA, treatmentB, app, session):
    treatmentA_dict = treatmentA.as_dict()
    codeA = treatmentA_dict['level_code']

    with app.test_request_context("/treatment/delete_treatment/{}".format(codeA), method="DELETE"):
        response = Delete().delete(codeA)
        assert response == treatmentA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/treatment/{}".format(codeA), method="GET"):
        try:
            response = TreatmentInfo().get(codeA)
        except Exception as e:
            assert e.code == 404
