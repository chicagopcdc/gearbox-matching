from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.input_type import InputType
from app.main.service.input_type_service import InputTypeService
from app.main.util import AlchemyEncoder
from app.main.util.dto import InputTypeDto


api = InputTypeDto.api
_input_type = InputTypeDto.input_type


@api.route('/<public_id>')
@api.param('public_id', 'The InputType identifier')
class InputTypeInfo(Resource):
    @api.doc('get a input_type')
    @api.marshal_with(_input_type)
    def get(self, public_id):
        input_type = InputTypeService.get_a_input_type(public_id)
        if not input_type:
            api.abort(404, message="input_type '{}' not found".format(public_id))
        else:
            return input_type.as_dict()


@api.route('/info')
class AllInputTypesInfo(Resource):
    def get(self):
        input_types = InputTypeService.get_all(InputType)
        try:
            if input_types:
                body = [r.as_dict() for r in input_types]
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
            api.abort(404, message="input_type table not found or has no data")


@api.route('/create_input_type')
class Create(Resource):
    @api.doc('create a new input_type')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = InputType()
        allowed_keys = template.as_dict().keys()

        new_input_type_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_input_type_dict.update({key:data[key]})
        try:
            response = InputTypeService.save_new_input_type(new_input_type_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_input_type/<public_id>')
@api.param('public_id', 'The InputType identifier')
class Update(Resource):
    @api.doc('update an existing input_type')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the input_type to be updated
        input_type = InputTypeService.get_a_input_type(public_id)
        if not input_type:
            api.abort(404, message="input_type '{}' not found".format(public_id))

        #set new key/input_types
        allowed_keys = input_type.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='name':
                    existing_input_type_with_new_code = InputTypeService.get_a_input_type(data[key])
                    if not existing_input_type_with_new_code:
                        setattr(input_type, key, data[key])
                    else:
                        #code input_types must be unique for each input_type
                        api.abort(409, message="input_type name '{}' is duplicate".format(data[key]))
                else:
                    setattr(input_type, key, data[key])
        try:
            InputTypeService.commit()
            return input_type.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_input_type/<public_id>')
@api.param('public_id', 'The InputType identifier')
class Delete(Resource):
    @api.doc('delete a input_type')
    def delete(self, public_id):
        input_type = InputTypeService.get_a_input_type(public_id)
        if not input_type:
            api.abort(404, message="input_type '{}' not found".format(public_id))

        try:
            InputTypeService.delete(input_type)
            return input_type.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
