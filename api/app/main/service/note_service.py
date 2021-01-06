import uuid
import datetime

from app.main import DbSession
from app.main.model.note import Note
from app.main.service import Services

class NoteService(Services):

    def save_new_note(self, data):
        note = self.get_a_note(self, data.get('id'))

        if not note:
            new_note = Note(
                id=data.get('id'),
                value=data.get('value'),
            )
            Services.save_changes(new_note)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Note already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_note(self, id):
        return DbSession.query(Note).filter(Note.id==id).first()
