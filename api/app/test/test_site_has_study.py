import json
import pytest

from app.main.model.site import Site
from app.main.controller.site_controller import SiteInfo, AllSitesInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def siteA():
    return Site(name = 'siteA', code = 'codeA', active = 0)


@pytest.fixture(scope="module")
def siteB():
    return Site(name = 'siteB', code = 'codeB', active = 0)


def test_setup(siteA, siteB, app, session):
    session.add(siteA)
    session.add(siteB)


def test_scope(siteA, siteB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/site/info", method="GET"):        
        response = AllSitesInfo().get()
        table_data = response.json['body']
        assert siteA.as_dict() in table_data
        assert siteB.as_dict() in table_data


def test_site_info(siteA, siteB, app, session):
    for code in [siteA.as_dict()['code'], siteB.as_dict()['code']]:
        with app.test_request_context("/site/{}".format(code), method="GET"):
            response = SiteInfo().get(code)
            assert code == response['code']


def test_all_sites_info(siteA, siteB, app, session):
    with app.test_request_context("/site/info", method="GET"):        
        response = AllSitesInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert siteA.as_dict() in table_data
        assert siteB.as_dict() in table_data


def test_create_site(app, session):
    payload= {'name': 'thisName', 'code': 'thisCode', 'active': 0}
    with app.test_request_context("/site/create_site", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/site/info", method="GET"):        
        response = AllSitesInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['code'] == 'thisCode':
                payload_seen = 1
        assert payload_seen == 1


def test_update_site(siteA, siteB, app, session):
    #basic update test
    siteA_dict = siteA.as_dict()
    codeA = siteA_dict['code']
    payload = {'name': siteA_dict['name']+'_updated'} #update the name for siteA
    with app.test_request_context("/site/update_site/{}".format(codeA), method="PUT", json=payload):
        response = Update().put(codeA)
        expected_response = siteA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/site/{}".format(codeA), method="GET"):
        current_siteA = SiteInfo().get(codeA)
        
    #attempt re-use of public_id/code (expected 409)
    siteB_dict = siteB.as_dict()
    codeB = siteB_dict['code']
    payload = {'code': codeB}
    with app.test_request_context("/site/update_site/{}".format(codeA), method="PUT", json=payload):
        try:
            response = Update().put(codeA)
        except Exception as e:
            assert e.code == 409    

def test_delete_site(siteA, siteB, app, session):
    siteA_dict = siteA.as_dict()
    codeA = siteA_dict['code']

    with app.test_request_context("/site/delete_site/{}".format(codeA), method="DELETE"):
        response = Delete().delete(codeA)
        assert response == siteA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/site/{}".format(codeA), method="GET"):
        try:
            response = SiteInfo().get(codeA)
        except Exception as e:
            assert e.code == 404
