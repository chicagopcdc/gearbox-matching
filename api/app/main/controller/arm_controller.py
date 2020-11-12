from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.arm import Arm
from app.main.service.arm_service import ArmService
from app.main.util import AlchemyEncoder
from app.main.util.dto import ArmDto


api = ArmDto.api
_arm = ArmDto.arm


@api.route('/<public_id>')
@api.param('public_id', 'The Arm identifier')
class ArmInfo(Resource):
    @api.doc('get a arm')
    @api.marshal_with(_arm)
    def get(self, public_id):
        arm = ArmService.get_a_arm(public_id)
        if not arm:
            api.abort(404, message="arm '{}' not found".format(public_id))
        else:
            return arm.as_dict()


@api.route('/info')
class AllArmsInfo(Resource):
    def get(self):
        arms = ArmService.get_all(Arm)
        try:
            if arms:
                body = [r.as_dict() for r in arms]
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
            api.abort(404, message="arm table not found or has no data")


@api.route('/create_arm')
class Create(Resource):
    @api.doc('create a new arm')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = Arm()
        allowed_keys = template.as_dict().keys()

        new_arm_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_arm_dict.update({key:data[key]})
        try:
            response = ArmService.save_new_arm(new_arm_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_arm/<public_id>')
@api.param('public_id', 'The Arm identifier')
class Update(Resource):
    @api.doc('update an existing arm')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the arm to be updated
        arm = ArmService.get_a_arm(public_id)
        if not arm:
            api.abort(404, message="arm '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = arm.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='code':
                    existing_arm_with_new_code = ArmService.get_a_arm(data[key])
                    if not existing_arm_with_new_code:
                        setattr(arm, key, data[key])
                    else:
                        #code values must be unique for each arm
                        api.abort(409, message="arm code '{}' is duplicate".format(data[key]))
                else:
                    setattr(arm, key, data[key])
        try:
            ArmService.commit()
            return arm.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_arm/<public_id>')
@api.param('public_id', 'The Arm identifier')
class Delete(Resource):
    @api.doc('delete a arm')
    def delete(self, public_id):
        arm = ArmService.get_a_arm(public_id)
        if not arm:
            api.abort(404, message="arm '{}' not found".format(public_id))

        try:
            ArmService.delete(arm)
            return arm.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
