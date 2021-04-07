import json
import pytest

from app.main.model.site_has_study import SiteHasStudy
from app.main.controller.site_has_study_controller import SiteHasStudyInfo, AllSiteHasStudiesInfo, Create, Delete


@pytest.fixture(scope="module")
def site_has_studyA():
    return SiteHasStudy(study_id = 1, site_id = 1, active = 0)


@pytest.fixture(scope="module")
def site_has_studyB():
    return SiteHasStudy(study_id = 2, site_id = 2, active = 0)


def test_setup(site_has_studyA, site_has_studyB, app, session):
    session.add(site_has_studyA)
    session.add(site_has_studyB)


def test_scope(site_has_studyA, site_has_studyB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/site_has_study/info", method="GET"):        
        response = AllSiteHasStudiesInfo().get()
        table_data = response.json['body']
        assert site_has_studyA.as_dict() in table_data
        assert site_has_studyB.as_dict() in table_data


def test_site_has_study_info(site_has_studyA, site_has_studyB, app, session):
    for shs in [site_has_studyA.as_dict(), site_has_studyB.as_dict()]:
        payload = {'study_id': shs.get('study_id'), 'site_id': shs.get('site_id')}
        with app.test_request_context("/site_has_study", method="GET", json=payload):
            response = SiteHasStudyInfo().get()
            r = json.loads(json.dumps(response), object_hook=lambda d: {k: int(v) if v and v.isdigit() else v for k, v in d.items()})
            assert shs == r


def test_all_site_has_studys_info(site_has_studyA, site_has_studyB, app, session):
    with app.test_request_context("/site_has_study/info", method="GET"):        
        response = AllSiteHasStudiesInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert site_has_studyA.as_dict() in table_data
        assert site_has_studyB.as_dict() in table_data


def test_create_site_has_study(app, session):
    payload= {'study_id': 3, 'site_id': 3}
    with app.test_request_context("/site_has_study/create_site_has_study", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/site_has_study/info", method="GET"):        
        response = AllSiteHasStudiesInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            pid = "{}*{}".format(row['study_id'], row['site_id'])
            if pid == "3*3":
                payload_seen = 1
        assert payload_seen == 1


def test_delete_site_has_study(site_has_studyA, site_has_studyB, app, session):
    shsA_dict = site_has_studyA.as_dict()
    payload = {'study_id': shsA_dict.get('study_id'), 'site_id': shsA_dict.get('site_id')}
    with app.test_request_context("/site_has_study/delete_site_has_study", method="DELETE", json=payload):
        response = Delete().delete()
        assert response == shsA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/site_has_study", method="GET", json=payload):
        try:
            response = SiteHasStudyInfo().get()
        except Exception as e:
            assert e.code == 404
