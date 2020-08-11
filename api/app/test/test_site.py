import json
import pytest

from app.main.model.site import Site
from app.main.controller.site_controller import SiteInfo, AllSitesInfo


@pytest.fixture(scope="module")
def siteA():
    return Site(name = 'siteA', code = 'codeA', active = 0)


@pytest.fixture(scope="module")
def siteB():
    return Site(name = 'siteB', code = 'codeB', active = 0)


def test_setup(siteA, siteB, app, session):
    session.add(siteA)
    session.add(siteB)
#    session.commit()

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
