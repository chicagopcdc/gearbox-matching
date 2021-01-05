import json
import pytest

from app.main.model.note import Note
from app.main.controller.note_controller import NoteInfo, AllNotesInfo, Create, Update, Delete


@pytest.fixture(scope="module")
def noteA():
    return Note(value = 'valueA')


@pytest.fixture(scope="module")
def noteB():
    return Note(value = 'valueB')


def test_setup(noteA, noteB, app, session):
    session.add(noteA)
    session.add(noteB)


def test_scope(noteA, noteB, app, session):
    #fixture scope should be greater than 'function', for use in later tests
    with app.test_request_context("/note/info", method="GET"):        
        response = AllNotesInfo().get()
        table_data = response.json['body']
        assert noteA.as_dict() in table_data
        assert noteB.as_dict() in table_data


def test_note_info(noteA, noteB, app, session):
    for public_id in [noteA.as_dict()['id'], noteB.as_dict()['id']]:
        with app.test_request_context("/note/{}".format(public_id), method="GET"):
            response = NoteInfo().get(public_id)
            assert public_id == response['id']


def test_all_notes_info(noteA, noteB, app, session):
    with app.test_request_context("/note/info", method="GET"):        
        response = AllNotesInfo().get()
        assert response.status_code == 200
        
        table_data = response.json['body']
        for row in table_data:
            print(isinstance(row, dict))
        assert noteA.as_dict() in table_data
        assert noteB.as_dict() in table_data


def test_create_note(app, session):
    payload= {'value': 'thisValue'}
    with app.test_request_context("/note/create_note", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201


def test_scope_again(app, session):
    with app.test_request_context("/note/info", method="GET"):        
        response = AllNotesInfo().get()
        table_data = response.json['body']
        payload_seen = 0
        for row in table_data:
            if row['value'] == 'thisValue':
                payload_seen = 1
        assert payload_seen == 1


def test_update_note(noteA, noteB, app, session):
    #basic update test
    noteA_dict = noteA.as_dict()
    idA = noteA_dict['id']
    payload = {'value': 'new_valueA'}
    with app.test_request_context("/note/update_note/{}".format(idA), method="PUT", json=payload):
        response = Update().put(idA)
        expected_response = noteA_dict
        expected_response.update(payload)
        assert response == expected_response
        

def test_delete_note(noteA, noteB, app, session):
    noteA_dict = noteA.as_dict()
    idA = noteA_dict['id']

    with app.test_request_context("/note/delete_note/{}".format(idA), method="DELETE"):
        response = Delete().delete(idA)
        assert response == noteA_dict

    #attempt to get what was deleted (expected 404)
    with app.test_request_context("/note/{}".format(idA), method="GET"):
        try:
            response = NoteInfo().get(idA)
        except Exception as e:
            assert e.code == 404
