import json
import pytest

from app.main.model.arm import Arm
from app.main.controller.arm_controller import ArmInfo, AllArmsInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def armA():
    return Arm(version_id = 1, study_id = 1, code = 'codeA')


@pytest.fixture(scope="module")
def armB():
    return Arm(version_id = 2, study_id = 1, code = 'codeB')


def test_setup(armA, armB, app, session):
    session.add(armA)
    session.add(armB)


def test_scope(armA, armB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/arm/info", method="GET"):        
        response = AllArmsInfo().get()
        table_data = response.json['body']
        assert armA.as_dict() in table_data
        assert armB.as_dict() in table_data


def test_arm_info(armA, armB, app, session):
    for public_id in [armA.as_dict()['code'], armB.as_dict()['code']]:
        with app.test_request_context("/arm/{}".format(public_id), method="GET"):
            response = ArmInfo().get(public_id)
            assert public_id == response['code']


def test_all_arms_info(armA, armB, app, session):
    with app.test_request_context("/arm/info", method="GET"):        
        response = AllArmsInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert armA.as_dict() in table_data
        assert armB.as_dict() in table_data


def test_create_arm(app, session):
    payload= {'version_id': 3, 'study_id': 2, 'code': 'thisCode', 'active': 0}
    with app.test_request_context("/arm/create_arm", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/arm/info", method="GET"):        
        response = AllArmsInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['code'] == 'thisCode':
                payload_seen = 1
        assert payload_seen == 1


def test_update_arm(armA, armB, app, session):
    #basic update test
    armA_dict = armA.as_dict()
    codeA = armA_dict['code']
    payload = {'active': 1} #update the arm to active
    with app.test_request_context("/arm/update_arm/{}".format(codeA), method="PUT", json=payload):
        response = Update().put(codeA)
        expected_response = armA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/arm/{}".format(codeA), method="GET"):
        current_armA = ArmInfo().get(codeA)
        
    #attempt re-use of public_id/code (expected 409)
    armB_dict = armB.as_dict()
    codeB = armB_dict['code']
    payload = {'code': codeB}
    with app.test_request_context("/arm/update_arm/{}".format(codeA), method="PUT", json=payload):
        try:
            response = Update().put(codeA)
        except Exception as e:
            assert e.code == 409    

def test_delete_arm(armA, armB, app, session):
    armA_dict = armA.as_dict()
    codeA = armA_dict['code']

    with app.test_request_context("/arm/delete_arm/{}".format(codeA), method="DELETE"):
        response = Delete().delete(codeA)
        assert response == armA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/arm/{}".format(codeA), method="GET"):
        try:
            response = ArmInfo().get(codeA)
        except Exception as e:
            assert e.code == 404
