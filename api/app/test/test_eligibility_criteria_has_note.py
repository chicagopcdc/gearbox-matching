import datetime
import json
import pytest

from app.main.model.eligibility_criteria_has_note import EligibilityCriteriaHasNote
from app.main.controller.eligibility_criteria_has_note_controller import EligibilityCriteriaHasNoteInfo, AllEligibilityCriteriaHasNotesInfo, Create, Delete


@pytest.fixture(scope="module")
def eligibility_criteria_has_noteA():
    return EligibilityCriteriaHasNote(eligibility_criteria_id = 1, note_id = 1)


@pytest.fixture(scope="module")
def eligibility_criteria_has_noteB():
    return EligibilityCriteriaHasNote(eligibility_criteria_id = 2, note_id = 2)


def test_setup(eligibility_criteria_has_noteA, eligibility_criteria_has_noteB, app, session):
    session.add(eligibility_criteria_has_noteA)
    session.add(eligibility_criteria_has_noteB)


def test_scope(eligibility_criteria_has_noteA, eligibility_criteria_has_noteB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/eligibility_criteria_has_note/info", method="GET"):        
        response = AllEligibilityCriteriaHasNotesInfo().get()
        table_data = response.json['body']
        assert eligibility_criteria_has_noteA.as_dict() in table_data
        assert eligibility_criteria_has_noteB.as_dict() in table_data


def test_eligibility_criteria_has_note_info(eligibility_criteria_has_noteA, eligibility_criteria_has_noteB, app, session):
    for echn in [eligibility_criteria_has_noteA.as_dict(), eligibility_criteria_has_noteB.as_dict()]:
        payload = {'eligibility_criteria_id': str(echn['eligibility_criteria_id']), 'note_id': str(echn['note_id'])}
        with app.test_request_context("/eligibility_criteria_has_note", method="GET", json=payload):
            response = EligibilityCriteriaHasNoteInfo().get()
            assert payload == response


def test_all_eligibility_criteria_has_notes_info(eligibility_criteria_has_noteA, eligibility_criteria_has_noteB, app, session):
    with app.test_request_context("/eligibility_criteria_has_note/info", method="GET"):        
        response = AllEligibilityCriteriaHasNotesInfo().get()
        assert response.status_code == 200
       
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert eligibility_criteria_has_noteA.as_dict() in table_data
        assert eligibility_criteria_has_noteB.as_dict() in table_data


def test_create_eligibility_criteria_has_note(app, session):
    payload = {'eligibility_criteria_id': 4, 'note_id': 3}
    with app.test_request_context("/eligibility_criteria_has_note/create_eligibility_criteria_has_note", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/eligibility_criteria_has_note/info", method="GET"):        
        response = AllEligibilityCriteriaHasNotesInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            pid = "{}*{}".format(row['eligibility_criteria_id'], row['note_id'])
            if pid == '4*3':
                payload_seen = 1
        assert payload_seen == 1


def test_delete_eligibility_criteria_has_note(eligibility_criteria_has_noteA, eligibility_criteria_has_noteB, app, session):
    echnA_dict = eligibility_criteria_has_noteA.as_dict()
    payload = {'eligibility_criteria_id': echnA_dict.get('eligibility_criteria_id'), 'note_id': echnA_dict.get('note_id')}
    
    with app.test_request_context("/eligibility_criteria_has_note/delete_eligibility_criteria_has_note", method="DELETE", json=payload):
        response = Delete().delete()
        assert response == echnA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/eligibility_criteria_has_note", method="GET", json=payload):
        try:
            response = EligibilityCriteriaHasNoteInfo().get()
        except Exception as e:
            assert e.code == 404
