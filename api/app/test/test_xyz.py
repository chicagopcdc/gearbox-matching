import json
import pytest

from app.main.model.xyz import Xyz
from app.main.controller.xyz_controller import XyzInfo, AllXyzsInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def xyzA():
    return Xyz(name = 'xyzA', code = 'codeA', active = 0)


@pytest.fixture(scope="module")
def xyzB():
    return Xyz(name = 'xyzB', code = 'codeB', active = 0)


def test_setup(xyzA, xyzB, app, session):
    session.add(xyzA)
    session.add(xyzB)


def test_scope(xyzA, xyzB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/xyz/info", method="GET"):        
        response = AllXyzsInfo().get()
        table_data = response.json['body']
        assert xyzA.as_dict() in table_data
        assert xyzB.as_dict() in table_data


def test_xyz_info(xyzA, xyzB, app, session):
    for public_id in [xyzA.as_dict()['code'], xyzB.as_dict()['code']]:
        with app.test_request_context("/xyz/{}".format(public_id), method="GET"):
            response = XyzInfo().get(public_id)
            assert public_id == response['code']


def test_all_xyzs_info(xyzA, xyzB, app, session):
    with app.test_request_context("/xyz/info", method="GET"):        
        response = AllXyzsInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert xyzA.as_dict() in table_data
        assert xyzB.as_dict() in table_data


def test_create_xyz(app, session):
    payload= {'name': 'thisName', 'code': 'thisCode', 'active': 0}
    with app.test_request_context("/xyz/create_xyz", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/xyz/info", method="GET"):        
        response = AllXyzsInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['code'] == 'thisCode':
                payload_seen = 1
        assert payload_seen == 1


def test_update_xyz(xyzA, xyzB, app, session):
    #basic update test
    xyzA_dict = xyzA.as_dict()
    codeA = xyzA_dict['code']
    payload = {'name': xyzA_dict['name']+'_updated'} #update the name for xyzA
    with app.test_request_context("/xyz/update_xyz/{}".format(codeA), method="PUT", json=payload):
        response = Update().put(codeA)
        expected_response = xyzA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/xyz/{}".format(codeA), method="GET"):
        current_xyzA = XyzInfo().get(codeA)
        
    #attempt re-use of public_id/code (expected 409)
    xyzB_dict = xyzB.as_dict()
    codeB = xyzB_dict['code']
    payload = {'code': codeB}
    with app.test_request_context("/xyz/update_xyz/{}".format(codeA), method="PUT", json=payload):
        try:
            response = Update().put(codeA)
        except Exception as e:
            assert e.code == 409    

def test_delete_xyz(xyzA, xyzB, app, session):
    xyzA_dict = xyzA.as_dict()
    codeA = xyzA_dict['code']

    with app.test_request_context("/xyz/delete_xyz/{}".format(codeA), method="DELETE"):
        response = Delete().delete(codeA)
        assert response == xyzA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/xyz/{}".format(codeA), method="GET"):
        try:
            response = XyzInfo().get(codeA)
        except Exception as e:
            assert e.code == 404
