from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.criterion_has_value import CriterionHasValue
from app.main.service.criterion_has_value_service import CriterionHasValueService
from app.main.util import AlchemyEncoder
from app.main.util.dto import CriterionHasValueDto


api = CriterionHasValueDto.api
_criterion_has_value = CriterionHasValueDto.criterion_has_value


@api.route('/<public_id>')
@api.param('public_id', 'The CriterionHasValue identifier')
class CriterionHasValueInfo(Resource):
    @api.doc('get a criterion_has_value')
    @api.marshal_with(_criterion_has_value)
    def get(self, public_id):
        criterion_has_value = CriterionHasValueService.get_a_criterion_has_value(self, public_id)
        if not criterion_has_value:
            api.abort(404, message="criterion_has_value '{}' not found".format(public_id))
        else:
            return criterion_has_value.as_dict()


@api.route('/info')
class AllCriterionHasValuesInfo(Resource):
    def get(self):
        criterion_has_values = CriterionHasValueService.get_all(CriterionHasValue)
        try:
            if criterion_has_values:
                body = [r.as_dict() for r in criterion_has_values]
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
            api.abort(404, message="criterion_has_value table not found or has no data")


@api.route('/create_criterion_has_value')
class Create(Resource):
    @api.doc('create a new criterion_has_value')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = CriterionHasValue()
        allowed_keys = template.as_dict().keys()

        new_criterion_has_value_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_criterion_has_value_dict.update({key:data[key]})
        try:
            response = CriterionHasValueService.save_new_criterion_has_value(CriterionHasValueService, new_criterion_has_value_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_criterion_has_value/<public_id>')
@api.param('public_id', 'The CriterionHasValue identifier')
class Update(Resource):
    @api.doc('update an existing criterion_has_value')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        criterion_has_value = CriterionHasValueService.get_a_criterion_has_value(self, public_id)
        if not criterion_has_value:
            api.abort(404, message="criterion_has_value '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = criterion_has_value.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                #DO NOT PREVENT PRIMARY KEY CHANGES
                setattr(criterion_has_value, key, data[key])
        try:
            CriterionHasValueService.commit()
            return criterion_has_value.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_criterion_has_value/<public_id>')
@api.param('public_id', 'The CriterionHasValue identifier')
class Delete(Resource):
    @api.doc('delete a criterion_has_value')
    def delete(self, public_id):
        criterion_has_value = CriterionHasValueService.get_a_criterion_has_value(self, public_id)
        if not criterion_has_value:
            api.abort(404, message="criterion_has_value '{}' not found".format(public_id))

        try:
            CriterionHasValueService.delete(criterion_has_value)
            return criterion_has_value.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
