from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.criterion import Criterion
from app.main.service.criterion_service import CriterionService
from app.main.util import AlchemyEncoder
from app.main.util.dto import CriterionDto


api = CriterionDto.api
_criterion = CriterionDto.criterion


@api.route('/<public_id>')
@api.param('public_id', 'The Criterion identifier')
class CriterionInfo(Resource):
    @api.doc('get a criterion')
    @api.marshal_with(_criterion)
    def get(self, public_id):
        criterion = CriterionService.get_a_criterion(public_id)
        if not criterion:
            api.abort(404, message="criterion '{}' not found".format(public_id))
        else:
            return criterion.as_dict()


@api.route('/info')
class AllCriterionsInfo(Resource):
    def get(self):
        criterions = CriterionService.get_all(Criterion)
        try:
            if criterions:
                body = [r.as_dict() for r in criterions]
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
            api.abort(404, message="criterion table not found or has no data")


@api.route('/create_criterion')
class Create(Resource):
    @api.doc('create a new criterion')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = Criterion()
        allowed_keys = template.as_dict().keys()

        new_criterion_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_criterion_dict.update({key:data[key]})
        try:
            response = CriterionService.save_new_criterion(new_criterion_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_criterion/<public_id>')
@api.param('public_id', 'The Criterion identifier')
class Update(Resource):
    @api.doc('update an existing criterion')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the criterion to be updated
        criterion = CriterionService.get_a_criterion(public_id)
        if not criterion:
            api.abort(404, message="criterion '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = criterion.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='code':
                    existing_criterion_with_new_code = CriterionService.get_a_criterion(data[key])
                    if not existing_criterion_with_new_code:
                        setattr(criterion, key, data[key])
                    else:
                        #code values must be unique for each criterion
                        api.abort(409, message="criterion code '{}' is duplicate".format(data[key]))
                else:
                    setattr(criterion, key, data[key])
        try:
            CriterionService.commit()
            return criterion.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_criterion/<public_id>')
@api.param('public_id', 'The Criterion identifier')
class Delete(Resource):
    @api.doc('delete a criterion')
    def delete(self, public_id):
        criterion = CriterionService.get_a_criterion(public_id)
        if not criterion:
            api.abort(404, message="criterion '{}' not found".format(public_id))

        try:
            CriterionService.delete(criterion)
            return criterion.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
