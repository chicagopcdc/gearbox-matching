from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.value import Value
from app.main.service.value_service import ValueService
from app.main.util import AlchemyEncoder
from app.main.util.dto import MatchDto


api = MatchDto.api
_value = MatchDto.value


@api.route('/eligibility_criteria')
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
            api.abort(404, message="criterion table not found or has no data")
