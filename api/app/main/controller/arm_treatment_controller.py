from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.arm_treatment import ArmTreatment
from app.main.service.arm_treatment_service import ArmTreatmentService
from app.main.util import AlchemyEncoder
from app.main.util.dto import ArmTreatmentDto


api = ArmTreatmentDto.api
_arm_treatment = ArmTreatmentDto.arm_treatment


@api.route('/<public_id>')
@api.param('public_id', 'The ArmTreatment identifier')
class ArmTreatmentInfo(Resource):
    @api.doc('get a arm_treatment')
    @api.marshal_with(_arm_treatment)
    def get(self, public_id):
        pid = public_id.split('-')
        data = {
            'arm_id': pid[0],
            'treatment_id': pid[1]
        }
        arm_treatment = ArmTreatmentService.get_a_arm_treatment(data)
        if not arm_treatment:
            api.abort(404, message="arm_treatment '{}' not found".format(data))
        else:
            return arm_treatment.as_dict()


@api.route('/info')
class AllArmTreatmentsInfo(Resource):
    def get(self):
        arm_treatments = ArmTreatmentService.get_all(ArmTreatment)
        try:
            if arm_treatments:
                body = [r.as_dict() for r in arm_treatments]
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
            api.abort(404, message="arm_treatment table not found or has no data")


@api.route('/create_arm_treatment')
class Create(Resource):
    @api.doc('create a new arm_treatment')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = ArmTreatment()
        allowed_keys = template.as_dict().keys()

        new_arm_treatment_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_arm_treatment_dict.update({key:data[key]})
        try:
            response = ArmTreatmentService.save_new_arm_treatment(new_arm_treatment_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_arm_treatment/<public_id>')
@api.param('public_id', 'The ArmTreatment identifier')
class Update(Resource):
    @api.doc('update an existing arm_treatment')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the arm_treatment to be updated
        pid = public_id.split('-')
        pid_data = {
            'arm_id': pid[0],
            'treatment_id': pid[1],
        }
        arm_treatment = ArmTreatmentService.get_a_arm_treatment(pid_data)
        if not arm_treatment:
            api.abort(404, message="arm_treatment '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = arm_treatment.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                #DO NOT PREVENT PRIMARY KEY CHANGES
                setattr(arm_treatment, key, data[key])
        try:
            ArmTreatmentService.commit()
            return arm_treatment.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_arm_treatment/<public_id>')
@api.param('public_id', 'The ArmTreatment identifier')
class Delete(Resource):
    @api.doc('delete a arm_treatment')
    def delete(self, public_id):
        pid = public_id.split('-')
        pid_data = {
            'arm_id': pid[0],
            'treatment_id': pid[1],
        }
        arm_treatment = ArmTreatmentService.get_a_arm_treatment(pid_data)
        if not arm_treatment:
            api.abort(404, message="arm_treatment '{}' not found".format(public_id))

        try:
            ArmTreatmentService.delete(arm_treatment)
            return arm_treatment.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
