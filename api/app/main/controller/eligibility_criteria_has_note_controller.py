from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.eligibility_criteria_has_note import EligibilityCriteriaHasNote
from app.main.service.eligibility_criteria_has_note_service import EligibilityCriteriaHasNoteService
from app.main.util import AlchemyEncoder
from app.main.util.dto import EligibilityCriteriaHasNoteDto


api = EligibilityCriteriaHasNoteDto.api
_eligibility_criteria_has_note = EligibilityCriteriaHasNoteDto.eligibility_criteria_has_note


@api.route('/<public_id>')
@api.param('public_id', 'The EligibilityCriteriaHasNote identifier')
class EligibilityCriteriaHasNoteInfo(Resource):
    @api.doc('get a eligibility_criteria_has_note')
    @api.marshal_with(_eligibility_criteria_has_note)
    def get(self, public_id):
        pid = public_id.split('-')
        data = {
            'eligibility_criteria_id': pid[0],
            'note_id': pid[1]
        }
        eligibility_criteria_has_note = EligibilityCriteriaHasNoteService.get_a_eligibility_criteria_has_note(self, data)
        if not eligibility_criteria_has_note:
            api.abort(404, message="eligibility_criteria_has_note '{}' not found".format(public_id))
        else:
            return eligibility_criteria_has_note.as_dict()


@api.route('/info')
class AllEligibilityCriteriaHasNotesInfo(Resource):
    def get(self):
        eligibility_criteria_has_notes = EligibilityCriteriaHasNoteService.get_all(EligibilityCriteriaHasNote)
        try:
            if eligibility_criteria_has_notes:
                body = [r.as_dict() for r in eligibility_criteria_has_notes]
            else:
                body = []
            return jsonify(
                {
                    "current_date": date.today().strftime("%B %d, %Y"),
                    "current_time": strftime("%H:%M:%S +0000", gmtime()),
                    "status": "OK",
                    "body": body
                }
            )
        except:
            api.abort(404, message="eligibility_criteria_has_note table not found or has no data")


@api.route('/create_eligibility_criteria_has_note')
class Create(Resource):
    @api.doc('create a new eligibility_criteria_has_note')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = EligibilityCriteriaHasNote()
        allowed_keys = template.as_dict().keys()

        new_eligibility_criteria_has_note_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_eligibility_criteria_has_note_dict.update({key:data[key]})
        try:
            response = EligibilityCriteriaHasNoteService.save_new_eligibility_criteria_has_note(EligibilityCriteriaHasNoteService, new_eligibility_criteria_has_note_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_eligibility_criteria_has_note/<public_id>')
@api.param('public_id', 'The EligibilityCriteriaHasNote identifier')
class Update(Resource):
    @api.doc('update an existing eligibility_criteria_has_note')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the eligibility_criteria_has_note to be updated
        pid = public_id.split('-')
        pid_data = {
            'eligibility_criteria_id': pid[0],
            'note_id': pid[1]
        }
        eligibility_criteria_has_note = EligibilityCriteriaHasNoteService.get_a_eligibility_criteria_has_note(self, pid_data)
        if not eligibility_criteria_has_note:
            api.abort(404, message="eligibility_criteria_has_note '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = eligibility_criteria_has_note.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                #DO NOT PREVENT PRIMARY KEY CHANGES
                setattr(eligibility_criteria_has_note, key, data[key])
        try:
            EligibilityCriteriaHasNoteService.commit()
            return eligibility_criteria_has_note.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_eligibility_criteria_has_note/<public_id>')
@api.param('public_id', 'The EligibilityCriteriaHasNote identifier')
class Delete(Resource):
    @api.doc('delete a eligibility_criteria_has_note')
    def delete(self, public_id):
        pid = public_id.split('-')
        pid_data = {
            'eligibility_criteria_id': pid[0],
            'note_id': pid[1]
        }
        eligibility_criteria_has_note = EligibilityCriteriaHasNoteService.get_a_eligibility_criteria_has_note(self, pid_data)
        if not eligibility_criteria_has_note:
            api.abort(404, message="eligibility_criteria_has_note '{}' not found".format(public_id))

        try:
            EligibilityCriteriaHasNoteService.delete(eligibility_criteria_has_note)
            return eligibility_criteria_has_note.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
