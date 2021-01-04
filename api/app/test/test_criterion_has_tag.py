import json
import pytest

from app.main.model.criterion_has_tag import CriterionHasTag
from app.main.controller.criterion_has_tag_controller import CriterionHasTagInfo, AllCriterionHasTagsInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def criterion_has_tagA():
    return CriterionHasTag(tag_id = 1, criterion_id = 1)


@pytest.fixture(scope="module")
def criterion_has_tagB():
    return CriterionHasTag(tag_id = 2, criterion_id = 2)


def test_setup(criterion_has_tagA, criterion_has_tagB, app, session):
    session.add(criterion_has_tagA)
    session.add(criterion_has_tagB)


def test_scope(criterion_has_tagA, criterion_has_tagB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/criterion_has_tag/info", method="GET"):        
        response = AllCriterionHasTagsInfo().get()
        table_data = response.json['body']
        assert criterion_has_tagA.as_dict() in table_data
        assert criterion_has_tagB.as_dict() in table_data


def test_criterion_has_tag_info(criterion_has_tagA, criterion_has_tagB, app, session):
    for cht in [criterion_has_tagA.as_dict(), criterion_has_tagB.as_dict()]:
        with app.test_request_context("/criterion_has_tag/{}-{}".format(cht['criterion_id'], cht['tag_id']), method="GET"):
            pid = "{}-{}".format(cht['criterion_id'], cht['tag_id'])
            response = CriterionHasTagInfo().get(pid)
            assert pid == "{}-{}".format(response['criterion_id'], response['tag_id'])


def test_all_criterion_has_tags_info(criterion_has_tagA, criterion_has_tagB, app, session):
    with app.test_request_context("/criterion_has_tag/info", method="GET"):        
        response = AllCriterionHasTagsInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert criterion_has_tagA.as_dict() in table_data
        assert criterion_has_tagB.as_dict() in table_data


def test_create_criterion_has_tag(app, session):
    payload= {'tag_id': 1, 'criterion_id': 2}
    with app.test_request_context("/criterion_has_tag/create_criterion_has_tag", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/criterion_has_tag/info", method="GET"):        
        response = AllCriterionHasTagsInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            pid = "{}-{}".format(row['tag_id'], row['criterion_id'])
            if pid == '1-2':
                payload_seen = 1
        assert payload_seen == 1


def test_update_criterion_has_tag(criterion_has_tagA, criterion_has_tagB, app, session):
    #basic update test
    criterion_has_tagA_dict = criterion_has_tagA.as_dict()
    pidA = "{}-{}".format(criterion_has_tagA_dict['tag_id'], criterion_has_tagA_dict['criterion_id'])
    payload = {'tag_id': 2, 'criterion_id': 1}
    with app.test_request_context("/criterion_has_tag/update_criterion_has_tag/{}".format(pidA), method="PUT", json=payload):
        response = Update().put(pidA)
        expected_response = criterion_has_tagA_dict
        expected_response.update(payload)
        assert response == expected_response
        

def test_delete_criterion_has_tag(criterion_has_tagA, criterion_has_tagB, app, session):
    criterion_has_tagA_dict = criterion_has_tagA.as_dict()
    pidA = "{}-{}".format(criterion_has_tagA_dict['criterion_id'], criterion_has_tagA_dict['tag_id'])

    with app.test_request_context("/criterion_has_tag/delete_criterion_has_tag/{}".format(pidA), method="DELETE"):
        response = Delete().delete(pidA)
        assert response == criterion_has_tagA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/criterion_has_tag/{}".format(pidA), method="GET"):
        try:
            response = CriterionHasTagInfo().get(pidA)
        except Exception as e:
            assert e.code == 404
