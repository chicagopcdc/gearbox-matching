from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.eligibility_criteria import EligibilityCriteria
from app.main.service.eligibility_criteria_service import EligibilityCriteriaService
from app.main.util import AlchemyEncoder
from app.main.util.dto import EligibilityCriteriaDto


api = EligibilityCriteriaDto.api
_eligibility_criteria = EligibilityCriteriaDto.eligibility_criteria


@api.route('/<public_id>')
@api.param('public_id', 'The EligibilityCriteria identifier')
class EligibilityCriteriaInfo(Resource):
    @api.doc('get a eligibility_criteria')
    @api.marshal_with(_eligibility_criteria)
    def get(self, public_id):
        eligibility_criteria = EligibilityCriteriaService.get_a_eligibility_criteria(self, public_id)
        if not eligibility_criteria:
            api.abort(404, message="eligibility_criteria '{}' not found".format(public_id))
        else:
            return eligibility_criteria.as_dict()


@api.route('/info')
class AllEligibilityCriteriasInfo(Resource):
    def get(self):
        eligibility_criterias = EligibilityCriteriaService.get_all(EligibilityCriteria)
        try:
            if eligibility_criterias:
                body = [r.as_dict() for r in eligibility_criterias]
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
            api.abort(404, message="eligibility_criteria table not found or has no data")


@api.route('/create_eligibility_criteria')
class Create(Resource):
    @api.doc('create a new eligibility_criteria')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = EligibilityCriteria()
        allowed_keys = template.as_dict().keys()

        new_eligibility_criteria_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_eligibility_criteria_dict.update({key:data[key]})
        try:
            response = EligibilityCriteriaService.save_new_eligibility_criteria(EligibilityCriteriaService, new_eligibility_criteria_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_eligibility_criteria/<public_id>')
@api.param('public_id', 'The EligibilityCriteria identifier')
class Update(Resource):
    @api.doc('update an existing eligibility_criteria')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the eligibility_criteria to be updated
        eligibility_criteria = EligibilityCriteriaService.get_a_eligibility_criteria(self, public_id)
        if not eligibility_criteria:
            api.abort(404, message="eligibility_criteria '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = eligibility_criteria.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='code':
                    existing_eligibility_criteria_with_new_code = EligibilityCriteriaService.get_a_eligibility_criteria(self, data[key])
                    if not existing_eligibility_criteria_with_new_code:
                        setattr(eligibility_criteria, key, data[key])
                    else:
                        #code values must be unique for each eligibility_criteria
                        api.abort(409, message="eligibility_criteria code '{}' is duplicate".format(data[key]))
                else:
                    setattr(eligibility_criteria, key, data[key])
        try:
            EligibilityCriteriaService.commit()
            return eligibility_criteria.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_eligibility_criteria/<public_id>')
@api.param('public_id', 'The EligibilityCriteria identifier')
class Delete(Resource):
    @api.doc('delete a eligibility_criteria')
    def delete(self, public_id):
        eligibility_criteria = EligibilityCriteriaService.get_a_eligibility_criteria(self, public_id)
        if not eligibility_criteria:
            api.abort(404, message="eligibility_criteria '{}' not found".format(public_id))

        try:
            EligibilityCriteriaService.delete(eligibility_criteria)
            return eligibility_criteria.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
