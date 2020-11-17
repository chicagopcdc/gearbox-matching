from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.treatment import Treatment
from app.main.service.treatment_service import TreatmentService
from app.main.util import AlchemyEncoder
from app.main.util.dto import TreatmentDto


api = TreatmentDto.api
_treatment = TreatmentDto.treatment


@api.route('/<public_id>')
@api.param('public_id', 'The Treatment identifier')
class TreatmentInfo(Resource):
    @api.doc('get a treatment')
    @api.marshal_with(_treatment)
    def get(self, public_id):
        treatment = TreatmentService.get_a_treatment(public_id)
        if not treatment:
            api.abort(404, message="treatment '{}' not found".format(public_id))
        else:
            return treatment.as_dict()


@api.route('/info')
class AllTreatmentsInfo(Resource):
    def get(self):
        treatments = TreatmentService.get_all(Treatment)
        try:
            if treatments:
                body = [r.as_dict() for r in treatments]
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
            api.abort(404, message="treatment table not found or has no data")


@api.route('/create_treatment')
class Create(Resource):
    @api.doc('create a new treatment')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = Treatment()
        allowed_keys = template.as_dict().keys()

        new_treatment_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_treatment_dict.update({key:data[key]})
        try:
            response = TreatmentService.save_new_treatment(new_treatment_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_treatment/<public_id>')
@api.param('public_id', 'The Treatment identifier')
class Update(Resource):
    @api.doc('update an existing treatment')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the treatment to be updated
        treatment = TreatmentService.get_a_treatment(public_id)
        if not treatment:
            api.abort(404, message="treatment '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = treatment.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='code':
                    existing_treatment_with_new_code = TreatmentService.get_a_treatment(data[key])
                    if not existing_treatment_with_new_code:
                        setattr(treatment, key, data[key])
                    else:
                        #code values must be unique for each treatment
                        api.abort(409, message="treatment code '{}' is duplicate".format(data[key]))
                else:
                    setattr(treatment, key, data[key])
        try:
            TreatmentService.commit()
            return treatment.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_treatment/<public_id>')
@api.param('public_id', 'The Treatment identifier')
class Delete(Resource):
    @api.doc('delete a treatment')
    def delete(self, public_id):
        treatment = TreatmentService.get_a_treatment(public_id)
        if not treatment:
            api.abort(404, message="treatment '{}' not found".format(public_id))

        try:
            TreatmentService.delete(treatment)
            return treatment.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
