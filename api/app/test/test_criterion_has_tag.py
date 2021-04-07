import json
import pytest

from app.main.model.criterion_has_tag import CriterionHasTag
from app.main.controller.criterion_has_tag_controller import CriterionHasTagInfo, AllCriterionHasTagsInfo, Create, Delete


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
        payload = {'criterion_id': str(cht.get('criterion_id')), 'tag_id': str(cht.get('tag_id'))}
        with app.test_request_context("/criterion_has_tag", method="GET", json=payload):
            response = CriterionHasTagInfo().get()
            assert payload == response


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
    payload= {'tag_id': 1, 'criterion_id': 3}
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
            pid = "{}*{}".format(row['tag_id'], row['criterion_id'])
            if pid == '1*3':
                payload_seen = 1
        assert payload_seen == 1


def test_delete_criterion_has_tag(criterion_has_tagA, criterion_has_tagB, app, session):
    chtA_dict = criterion_has_tagA.as_dict()
    payload = {'criterion_id': chtA_dict.get('criterion_id'), 'tag_id': chtA_dict.get('tag_id')}

    with app.test_request_context("/criterion_has_tag/delete_criterion_has_tag", method="DELETE", json=payload):
        response = Delete().delete()
        assert response == chtA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/criterion_has_tag", method="GET", json=payload):
        try:
            response = CriterionHasTagInfo().get()
        except Exception as e:
            assert e.code == 404
