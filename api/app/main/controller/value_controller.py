from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.value import Value
from app.main.service.value_service import ValueService
from app.main.util import AlchemyEncoder
from app.main.util.dto import ValueDto


api = ValueDto.api
_value = ValueDto.value


@api.route('/<public_id>')
@api.param('public_id', 'The Value identifier')
class ValueInfo(Resource):
    @api.doc('get a value')
    @api.marshal_with(_value)
    def get(self, public_id):
        value = ValueService.get_a_value(public_id)
        if not value:
            api.abort(404, message="value '{}' not found".format(public_id))
        else:
            return value.as_dict()


@api.route('/info')
class AllValuesInfo(Resource):
    def get(self):
        values = ValueService.get_all(Value)
        try:
            if values:
                body = [r.as_dict() for r in values]
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
            api.abort(404, message="value table not found or has no data")


@api.route('/create_value')
class Create(Resource):
    @api.doc('create a new value')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = Value()
        allowed_keys = template.as_dict().keys()

        new_value_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_value_dict.update({key:data[key]})
        try:
            response = ValueService.save_new_value(new_value_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_value/<public_id>')
@api.param('public_id', 'The Value identifier')
class Update(Resource):
    @api.doc('update an existing value')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the value to be updated
        value = ValueService.get_a_value(public_id)
        if not value:
            api.abort(404, message="value '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = value.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='code':
                    existing_value_with_new_code = ValueService.get_a_value(data[key])
                    if not existing_value_with_new_code:
                        setattr(value, key, data[key])
                    else:
                        #code values must be unique for each value
                        api.abort(409, message="value code '{}' is duplicate".format(data[key]))
                else:
                    setattr(value, key, data[key])
        try:
            ValueService.commit()
            return value.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_value/<public_id>')
@api.param('public_id', 'The Value identifier')
class Delete(Resource):
    @api.doc('delete a value')
    def delete(self, public_id):
        value = ValueService.get_a_value(public_id)
        if not value:
            api.abort(404, message="value '{}' not found".format(public_id))

        try:
            ValueService.delete(value)
            return value.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e