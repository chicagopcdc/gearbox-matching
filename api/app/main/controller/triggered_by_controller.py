from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.triggered_by import TriggeredBy
from app.main.service.triggered_by_service import TriggeredByService
from app.main.util import AlchemyEncoder
from app.main.util.dto import TriggeredByDto


api = TriggeredByDto.api
_triggered_by = TriggeredByDto.triggered_by


@api.route('/<public_id>')
@api.param('public_id', 'The TriggeredBy identifier')
class TriggeredByInfo(Resource):
    @api.doc('get a triggered_by')
    @api.marshal_with(_triggered_by)
    def get(self, public_id):
        triggered_by = TriggeredByService.get_a_triggered_by(self, public_id)
        if not triggered_by:
            api.abort(404, message="triggered_by '{}' not found".format(public_id))
        else:
            return triggered_by.as_dict()


@api.route('/info')
class AllTriggeredBysInfo(Resource):
    def get(self):
        triggered_bys = TriggeredByService.get_all(TriggeredBy)
        try:
            if triggered_bys:
                body = [r.as_dict() for r in triggered_bys]
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
            api.abort(404, message="triggered_by table not found or has no data")


@api.route('/create_triggered_by')
class Create(Resource):
    @api.doc('create a new triggered_by')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = TriggeredBy()
        allowed_keys = template.as_dict().keys()

        new_triggered_by_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_triggered_by_dict.update({key:data[key]})
        try:
            response = TriggeredByService.save_new_triggered_by(TriggeredByService, new_triggered_by_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_triggered_by/<public_id>')
@api.param('public_id', 'The TriggeredBy identifier')
class Update(Resource):
    @api.doc('update an existing triggered_by')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        triggered_by = TriggeredByService.get_a_triggered_by(self, public_id)
        if not triggered_by:
            api.abort(404, message="triggered_by '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = triggered_by.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                #DO NOT PREVENT PRIMARY KEY CHANGES
                setattr(triggered_by, key, data[key])
        try:
            TriggeredByService.commit()
            return triggered_by.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_triggered_by/<public_id>')
@api.param('public_id', 'The TriggeredBy identifier')
class Delete(Resource):
    @api.doc('delete a triggered_by')
    def delete(self, public_id):
        triggered_by = TriggeredByService.get_a_triggered_by(self, public_id)
        if not triggered_by:
            api.abort(404, message="triggered_by '{}' not found".format(public_id))

        try:
            TriggeredByService.delete(triggered_by)
            return triggered_by.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
