from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.note import Note
from app.main.service.note_service import NoteService
from app.main.util import AlchemyEncoder
from app.main.util.dto import NoteDto


api = NoteDto.api
_note = NoteDto.note


@api.route('/<public_id>')
@api.param('public_id', 'The Note identifier')
class NoteInfo(Resource):
    @api.doc('get a note')
    @api.marshal_with(_note)
    def get(self, public_id):
        note = NoteService.get_a_note(public_id)
        if not note:
            api.abort(404, message="note '{}' not found".format(public_id))
        else:
            return note.as_dict()


@api.route('/info')
class AllNotesInfo(Resource):
    def get(self):
        notes = NoteService.get_all(Note)
        try:
            if notes:
                body = [r.as_dict() for r in notes]
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
            api.abort(404, message="note table not found or has no data")


@api.route('/create_note')
class Create(Resource):
    @api.doc('create a new note')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = Note()
        allowed_keys = template.as_dict().keys()

        new_note_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_note_dict.update({key:data[key]})
        try:
            response = NoteService.save_new_note(new_note_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_note/<public_id>')
@api.param('public_id', 'The Note identifier')
class Update(Resource):
    @api.doc('update an existing note')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the note to be updated
        note = NoteService.get_a_note(public_id)
        if not note:
            api.abort(404, message="note '{}' not found".format(public_id))

        #set new key/notes
        allowed_keys = note.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
               setattr(note, key, data[key])
        try:
            NoteService.commit()
            return note.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_note/<public_id>')
@api.param('public_id', 'The Note identifier')
class Delete(Resource):
    @api.doc('delete a note')
    def delete(self, public_id):
        note = NoteService.get_a_note(public_id)
        if not note:
            api.abort(404, message="note '{}' not found".format(public_id))

        try:
            NoteService.delete(note)
            return note.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
