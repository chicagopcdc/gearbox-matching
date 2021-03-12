from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.input_type_has_value import InputTypeHasValue
from app.main.service.input_type_has_value_service import InputTypeHasValueService
from app.main.util import AlchemyEncoder
from app.main.util.dto import InputTypeHasValueDto


api = InputTypeHasValueDto.api
_input_type_has_value = InputTypeHasValueDto.input_type_has_value


@api.route('/<public_id>')
@api.param('public_id', 'The InputTypeHasValue identifier')
class InputTypeHasValueInfo(Resource):
    @api.doc('get a input_type_has_value')
    @api.marshal_with(_input_type_has_value)
    def get(self, public_id):
        pid = public_id.split('-')
        data = {
            'criterion_id': pid[0],
            'eligibility_criteria_id': pid[1],
            'value_id': pid[2],            
        }
        input_type_has_value = InputTypeHasValueService.get_a_input_type_has_value(self, data)
        if not input_type_has_value:
            api.abort(404, message="input_type_has_value '{}' not found".format(public_id))
        else:
            return input_type_has_value.as_dict()


@api.route('/info')
class AllInputTypeHasValuesInfo(Resource):
    def get(self):
        input_type_has_values = InputTypeHasValueService.get_all(InputTypeHasValue)
        try:
            if input_type_has_values:
                body = [r.as_dict() for r in input_type_has_values]
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
            api.abort(404, message="input_type_has_value table not found or has no data")


@api.route('/create_input_type_has_value')
class Create(Resource):
    @api.doc('create a new input_type_has_value')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = InputTypeHasValue()
        allowed_keys = template.as_dict().keys()

        new_input_type_has_value_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_input_type_has_value_dict.update({key:data[key]})
        try:
            response = InputTypeHasValueService.save_new_input_type_has_value(InputTypeHasValueService, new_input_type_has_value_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_input_type_has_value/<public_id>')
@api.param('public_id', 'The InputTypeHasValue identifier')
class Update(Resource):
    @api.doc('update an existing input_type_has_value')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the input_type_has_value to be updated
        pid = public_id.split('-')
        pid_data = {
            'criterion_id': pid[0],
            'eligibility_criteria_id': pid[1],
            'value_id': pid[2],
        }
        input_type_has_value = InputTypeHasValueService.get_a_input_type_has_value(self, pid_data)
        if not input_type_has_value:
            api.abort(404, message="input_type_has_value '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = input_type_has_value.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                #DO NOT PREVENT PRIMARY KEY CHANGES
                setattr(input_type_has_value, key, data[key])
        try:
            InputTypeHasValueService.commit()
            return input_type_has_value.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_input_type_has_value/<public_id>')
@api.param('public_id', 'The InputTypeHasValue identifier')
class Delete(Resource):
    @api.doc('delete a input_type_has_value')
    def delete(self, public_id):
        pid = public_id.split('-')
        pid_data = {
            'criterion_id': pid[0],
            'eligibility_criteria_id': pid[1],
            'value_id': pid[2],
        }
        input_type_has_value = InputTypeHasValueService.get_a_input_type_has_value(self, pid_data)
        if not input_type_has_value:
            api.abort(404, message="input_type_has_value '{}' not found".format(public_id))

        try:
            InputTypeHasValueService.delete(input_type_has_value)
            return input_type_has_value.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
