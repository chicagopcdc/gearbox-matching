import uuid
import datetime

from app.main import DbSession
from app.main.model.eligibility_criteria_has_note import EligibilityCriteriaHasNote
from app.main.service import Services

class EligibilityCriteriaHasNoteService(Services):

    def save_new_eligibility_criteria_has_note(self, data):
        eligibility_criteria_has_note = self.get_a_eligibility_criteria_has_note(self, data)

        if not eligibility_criteria_has_note:
            new_eligibility_criteria_has_note = EligibilityCriteriaHasNote(
                eligibility_criteria_id=data.get('eligibility_criteria_id'),
                note_id=data.get('note_id'),
            )
            Services.save_changes(new_eligibility_criteria_has_note)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'EligibilityCriteriaHasNote already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_eligibility_criteria_has_note(self, data):
        return DbSession.query(EligibilityCriteriaHasNote).filter(
            EligibilityCriteriaHasNote.eligibility_criteria_id==data.get('eligibility_criteria_id'), 
            EligibilityCriteriaHasNote.note_id==data.get('note_id'),
        ).first()
