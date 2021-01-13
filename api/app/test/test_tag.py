import json
import pytest

from app.main.model.tag import Tag
from app.main.controller.tag_controller import TagInfo, AllTagsInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def tagA():
    return Tag(code = 'codeA')


@pytest.fixture(scope="module")
def tagB():
    return Tag(code = 'codeB')


def test_setup(tagA, tagB, app, session):
    session.add(tagA)
    session.add(tagB)


def test_scope(tagA, tagB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/tag/info", method="GET"):        
        response = AllTagsInfo().get()
        table_data = response.json['body']
        assert tagA.as_dict() in table_data
        assert tagB.as_dict() in table_data


def test_tag_info(tagA, tagB, app, session):
    for public_id in [tagA.as_dict()['code'], tagB.as_dict()['code']]:
        with app.test_request_context("/tag/{}".format(public_id), method="GET"):
            response = TagInfo().get(public_id)
            assert public_id == response['code']


def test_all_tags_info(tagA, tagB, app, session):
    with app.test_request_context("/tag/info", method="GET"):        
        response = AllTagsInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert tagA.as_dict() in table_data
        assert tagB.as_dict() in table_data


def test_create_tag(app, session):
    payload= {'code': 'thisCode'}
    with app.test_request_context("/tag/create_tag", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/tag/info", method="GET"):        
        response = AllTagsInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['code'] == 'thisCode':
                payload_seen = 1
        assert payload_seen == 1


def test_update_tag(tagA, tagB, app, session):
    #basic update test
    tagA_dict = tagA.as_dict()
    codeA = tagA_dict['code']
    payload = {'type': 'this_type'}
    with app.test_request_context("/tag/update_tag/{}".format(codeA), method="PUT", json=payload):
        response = Update().put(codeA)
        expected_response = tagA_dict
        expected_response.update(payload)
        assert response == expected_response
        
    with app.test_request_context("/tag/{}".format(codeA), method="GET"):
        current_tagA = TagInfo().get(codeA)
        
    #attempt re-use of public_id/code (expected 409)
    tagB_dict = tagB.as_dict()
    codeB = tagB_dict['code']
    payload = {'code': codeB}
    with app.test_request_context("/tag/update_tag/{}".format(codeA), method="PUT", json=payload):
        try:
            response = Update().put(codeA)
        except Exception as e:
            assert e.code == 409    

def test_delete_tag(tagA, tagB, app, session):
    tagA_dict = tagA.as_dict()
    codeA = tagA_dict['code']

    with app.test_request_context("/tag/delete_tag/{}".format(codeA), method="DELETE"):
        response = Delete().delete(codeA)
        assert response == tagA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/tag/{}".format(codeA), method="GET"):
        try:
            response = TagInfo().get(codeA)
        except Exception as e:
            assert e.code == 404
