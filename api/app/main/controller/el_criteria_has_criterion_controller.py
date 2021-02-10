from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.el_criteria_has_criterion import ElCriteriaHasCriterion
from app.main.service.el_criteria_has_criterion_service import ElCriteriaHasCriterionService
from app.main.util import AlchemyEncoder
from app.main.util.dto import ElCriteriaHasCriterionDto


api = ElCriteriaHasCriterionDto.api
_el_criteria_has_criterion = ElCriteriaHasCriterionDto.el_criteria_has_criterion


@api.route('/<public_id>')
@api.param('public_id', 'The ElCriteriaHasCriterion identifier')
class ElCriteriaHasCriterionInfo(Resource):
    @api.doc('get a el_criteria_has_criterion')
    @api.marshal_with(_el_criteria_has_criterion)
    def get(self, public_id):
        pid = public_id.split('-')
        data = {
            'criterion_id': pid[0],
            'eligibility_criteria_id': pid[1],
            'value_id': pid[2],            
        }
        el_criteria_has_criterion = ElCriteriaHasCriterionService.get_a_el_criteria_has_criterion(self, data)
        if not el_criteria_has_criterion:
            api.abort(404, message="el_criteria_has_criterion '{}' not found".format(public_id))
        else:
            return el_criteria_has_criterion.as_dict()


@api.route('/info')
class AllElCriteriaHasCriterionsInfo(Resource):
    def get(self):
        el_criteria_has_criterions = ElCriteriaHasCriterionService.get_all(ElCriteriaHasCriterion)
        try:
            if el_criteria_has_criterions:
                body = [r.as_dict() for r in el_criteria_has_criterions]
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
            api.abort(404, message="el_criteria_has_criterion table not found or has no data")


@api.route('/create_el_criteria_has_criterion')
class Create(Resource):
    @api.doc('create a new el_criteria_has_criterion')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = ElCriteriaHasCriterion()
        allowed_keys = template.as_dict().keys()

        new_el_criteria_has_criterion_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_el_criteria_has_criterion_dict.update({key:data[key]})
        try:
            response = ElCriteriaHasCriterionService.save_new_el_criteria_has_criterion(ElCriteriaHasCriterionService, new_el_criteria_has_criterion_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_el_criteria_has_criterion/<public_id>')
@api.param('public_id', 'The ElCriteriaHasCriterion identifier')
class Update(Resource):
    @api.doc('update an existing el_criteria_has_criterion')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the el_criteria_has_criterion to be updated
        pid = public_id.split('-')
        pid_data = {
            'criterion_id': pid[0],
            'eligibility_criteria_id': pid[1],
            'value_id': pid[2],
        }
        el_criteria_has_criterion = ElCriteriaHasCriterionService.get_a_el_criteria_has_criterion(self, pid_data)
        if not el_criteria_has_criterion:
            api.abort(404, message="el_criteria_has_criterion '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = el_criteria_has_criterion.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                #DO NOT PREVENT PRIMARY KEY CHANGES
                setattr(el_criteria_has_criterion, key, data[key])
        try:
            ElCriteriaHasCriterionService.commit()
            return el_criteria_has_criterion.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_el_criteria_has_criterion/<public_id>')
@api.param('public_id', 'The ElCriteriaHasCriterion identifier')
class Delete(Resource):
    @api.doc('delete a el_criteria_has_criterion')
    def delete(self, public_id):
        pid = public_id.split('-')
        pid_data = {
            'criterion_id': pid[0],
            'eligibility_criteria_id': pid[1],
            'value_id': pid[2],
        }
        el_criteria_has_criterion = ElCriteriaHasCriterionService.get_a_el_criteria_has_criterion(self, pid_data)
        if not el_criteria_has_criterion:
            api.abort(404, message="el_criteria_has_criterion '{}' not found".format(public_id))

        try:
            ElCriteriaHasCriterionService.delete(el_criteria_has_criterion)
            return el_criteria_has_criterion.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
