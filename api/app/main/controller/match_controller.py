from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime

from app.main.util import AlchemyEncoder
from app.main.util.dto import MatchDto

from app.main.model.study import Study
from app.main.service.study_service import StudyService

from app.main.model.value import Value
from app.main.service.value_service import ValueService

from app.main.model.algorithm_engine import AlgorithmEngine
from app.main.service.algorithm_engine_service import AlgorithmEngineService

import app.main.service.match_conditions as mc


api = MatchDto.api
_study = MatchDto.study
_value = MatchDto.value
_algorithm_engine = MatchDto.algorithm_engine


@api.route('/studies')
class MatchStudies(Resource):
    def get(self):
        studies = StudyService.get_all(Study)
        try:
            if studies:
                rows = [x.as_dict() for x in studies]
                body=[]
                for row in rows:
                    if row.get('active'):
                        data = {
                            'id': row.get('id'),
                            'title': row.get('name'),
                            'group': row.get('group'),
                            'location': row.get('location'),
                            }
                        body.append(data)
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
            api.abort(404, message="study table not found or has no data")


@api.route('/eligibility-criteria')
class MatchEligibilityCriteria(Resource):
    def get(self):
        values = ValueService.get_all(Value)
        try:
            if values:
                vals = [v.as_dict() for v in values]
                body=[]
                id = 0
                fieldId = 0
                for val in vals:
                    if val.get('active'):
                        row = {
                            'id': id,
                            'fieldId': fieldId,
                            }
                        id+=1
                        fieldId+=1

                        #assumes that these are mutually exclusive
                        if val.get('upper_threshold'):
                            fieldValue = val.get('upper_threshold')
                            if val.get('upper_modifier'):
                                operator = val.get('upper_modifier')
                        elif val.get('lower_threshold'):
                            fieldValue = val.get('lower_threshold')
                            if val.get('lower_modifier'):
                                operator = val.get('lower_modifier')
                        elif val.get('value_bool'):
                            raw_val = val.get('value_bool')
                            if raw_val in ["TRUE", "True", "true", True, '1', 1]:
                                fieldValue = True
                            elif raw_val in ["FALSE", "False", "False", False, '0', 0]:
                                fieldValue = False
                            operator = 'eq'
                        row.update({'fieldValue': fieldValue, 'operator': operator})
                        body.append(row)
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
            api.abort(404, message="info not found or has no data")


@api.route('/match-conditions')
class MatchMatchConditions(Resource):
    def get(self):
        all_algo_engs = AlgorithmEngineService.get_all(AlgorithmEngine)
        try:
            if all_algo_engs:
                #get parent_paths (pps), and corresponding operators (ops)
                pps = [x.as_dict()['parent_path'] for x in all_algo_engs]
                ops = [x.as_dict()['operator'] for x in all_algo_engs]
                #append another fake OR to trigger the final row to go in
                pps.append('terminus')
                ops.append('OR')

                full_paths = mc.get_full_paths(pps, ops)
                X = mc.merged(full_paths)
                R = mc.format(X)
                
                body = R
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
            api.abort(404, message="algorithm_engine table not found or has no data")
