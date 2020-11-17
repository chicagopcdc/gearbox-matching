import json
import pytest

from app.main.model.arm_treatment import ArmTreatment
from app.main.controller.arm_treatment_controller import ArmTreatmentInfo, AllArmTreatmentsInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def arm_treatmentA():
    return ArmTreatment(arm_id = 1, treatment_id = 1)


@pytest.fixture(scope="module")
def arm_treatmentB():
    return ArmTreatment(arm_id = 2, treatment_id = 1)


def test_setup(arm_treatmentA, arm_treatmentB, app, session):
    session.add(arm_treatmentA)
    session.add(arm_treatmentB)


def test_scope(arm_treatmentA, arm_treatmentB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/arm_treatment/info", method="GET"):        
        response = AllArmTreatmentsInfo().get()
        table_data = response.json['body']
        assert arm_treatmentA.as_dict() in table_data
        assert arm_treatmentB.as_dict() in table_data


def test_arm_treatment_info(arm_treatmentA, arm_treatmentB, app, session):
    for public_id in [arm_treatmentA.as_dict(), arm_treatmentB.as_dict()]:
        with app.test_request_context("/arm_treatment/{}-{}".format(public_id['arm_id'], public_id['treatment_id']), method="GET"):
            pid = "{}-{}".format(public_id['arm_id'], public_id['treatment_id'])
            response = ArmTreatmentInfo().get(pid)
            assert pid == "{}-{}".format(response['arm_id'], response['treatment_id'])


def test_all_arm_treatments_info(arm_treatmentA, arm_treatmentB, app, session):
    with app.test_request_context("/arm_treatment/info", method="GET"):        
        response = AllArmTreatmentsInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert arm_treatmentA.as_dict() in table_data
        assert arm_treatmentB.as_dict() in table_data


def test_create_arm_treatment(app, session):
    payload= {'arm_id': 2, 'treatment_id': 2}
    with app.test_request_context("/arm_treatment/create_arm_treatment", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/arm_treatment/info", method="GET"):        
        response = AllArmTreatmentsInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['arm_id']==2 and row['treatment_id']==2:
                payload_seen = 1
        assert payload_seen == 1


def test_update_arm_treatment(arm_treatmentA, arm_treatmentB, app, session):
    #basic update test
    arm_treatmentA_dict = arm_treatmentA.as_dict()
    pidA = "{}-{}".format(arm_treatmentA_dict['arm_id'], arm_treatmentA_dict['treatment_id'])
    payload = {'active': 1}
    with app.test_request_context("/arm_treatment/update_arm_treatment/{}".format(pidA), method="PUT", json=payload):
        response = Update().put(pidA)
        expected_response = arm_treatmentA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/arm_treatment/{}".format(pidA), method="GET"):
        current_arm_treatmentA = ArmTreatmentInfo().get(pidA)


def test_delete_arm_treatment(arm_treatmentA, arm_treatmentB, app, session):
    arm_treatmentA_dict = arm_treatmentA.as_dict()
    pidA = "{}-{}".format(arm_treatmentA_dict['arm_id'], arm_treatmentA_dict['treatment_id'])

    with app.test_request_context("/arm_treatment/delete_arm_treatment/{}".format(pidA), method="DELETE"):
        response = Delete().delete(pidA)
        assert response == arm_treatmentA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/arm_treatment/{}".format(pidA), method="GET"):
        try:
            response = ArmTreatmentInfo().get(pidA)
        except Exception as e:
            assert e.code == 404
