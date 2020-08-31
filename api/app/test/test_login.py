import json
import pytest

from app.main.model.login import Login
from app.main.controller.login_controller import LoginInfo, AllLoginsInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def loginA():
    return Login(sub_id = '19', refresh_token = 'Thequickbrownfoxjumpsoverthelazydog0123456789', iat = "2020-01-01T00:00:00.000", exp = "2021-01-01T00:00:00.000")


@pytest.fixture(scope="module")
def loginB():
    return Login(sub_id = '29', refresh_token = 'Brownthequickoverthelazyfoxdogjumps9876543210', iat = "2020-06-30T12:00:00.000", exp = "2021-06-30T12:00:00.000")


def test_setup(loginA, loginB, app, session):
    session.add(loginA)
    session.add(loginB)
#    session.commit()

def test_scope(loginA, loginB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/login/info", method="GET"):        
        response = AllLoginsInfo().get()
        table_data = response.json['body']
        assert loginA.as_dict() in table_data
        assert loginB.as_dict() in table_data


def test_login_info(loginA, loginB, app, session):
    for sub_id in [loginA.as_dict()['sub_id'], loginB.as_dict()['sub_id']]:
        with app.test_request_context("/login/{}".format(sub_id), method="GET"):
            response = LoginInfo().get(sub_id)
            assert sub_id == response['sub_id']


def test_all_logins_info(loginA, loginB, app, session):
    with app.test_request_context("/login/info", method="GET"):        
        response = AllLoginsInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert loginA.as_dict() in table_data
        assert loginB.as_dict() in table_data


def test_create_login(loginA, loginB, app, session):
    payload= {"sub_id": '11', "refresh_token": "foxescatsandlazydogs999", "iat": "0000-01-01T00:00:00.000", "exp": "0001-01-01T00:00:00.000"}
    with app.test_request_context("/login/create_login", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/login/info", method="GET"):        
        response = AllLoginsInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['sub_id'] == '11': #<same as in the above test
                payload_seen = 1
        assert payload_seen == 1


def test_update_login(loginA, loginB, app, session):
    #basic update test
    loginA_dict = loginA.as_dict()
    sub_idA = loginA_dict['sub_id']
    payload = {'refresh_token': loginA_dict['refresh_token']+'_updated'} #update the token for loginA
    with app.test_request_context("/login/update_login/{}".format(sub_idA), method="PUT", json=payload):
        response = Update().put(sub_idA)
        expected_response = loginA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/login/{}".format(sub_idA), method="GET"):
        current_loginA = LoginInfo().get(sub_idA)
        
    #attempt re-use of sub_id (expected 409)
    loginB_dict = loginB.as_dict()
    sub_idB = loginB_dict['sub_id']
    payload = {'sub_id': sub_idB}
    with app.test_request_context("/login/update_login/{}".format(sub_idA), method="PUT", json=payload):
        try:
            response = Update().put(sub_idA)
        except Exception as e:
            assert e.code == 409

def test_delete_login(loginA, loginB, app, session):
    loginA_dict = loginA.as_dict()
    sub_idA = loginA_dict['sub_id']

    with app.test_request_context("/login/delete_login/{}".format(sub_idA), method="DELETE"):
        response = Delete().delete(sub_idA)
        assert response == loginA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/login/{}".format(sub_idA), method="GET"):
        try:
            response = LoginInfo().get(sub_idA)
        except Exception as e:
            assert e.code == 404
