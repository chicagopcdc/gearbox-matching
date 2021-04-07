from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime

from app.main.util import AlchemyEncoder
from app.main.util.dto import MatchDto

from app.main.model.study import Study
from app.main.service.study_service import StudyService

from app.main.model.study_links import StudyLinks
from app.main.service.study_links_service import StudyLinksService

from app.main.model.value import Value
from app.main.service.value_service import ValueService

from app.main.model.algorithm_engine import AlgorithmEngine
from app.main.service.algorithm_engine_service import AlgorithmEngineService

from app.main.model.tag import Tag
from app.main.service.tag_service import TagService

from app.main.model.display_rules import DisplayRules
from app.main.service.display_rules_service import DisplayRulesService

from app.main.model.input_type import InputType
from app.main.service.input_type_service import InputTypeService

from app.main.model.el_criteria_has_criterion import ElCriteriaHasCriterion
from app.main.service.el_criteria_has_criterion_service import ElCriteriaHasCriterionService

from app.main.model.criterion import Criterion
from app.main.service.criterion_service import CriterionService

from app.main.model.criterion_has_tag import CriterionHasTag
from app.main.service.criterion_has_tag_service import CriterionHasTagService

from app.main.model.criterion_has_value import CriterionHasValue
from app.main.service.criterion_has_value_service import CriterionHasValueService

from app.main.model.triggered_by import TriggeredBy
from app.main.service.triggered_by_service import TriggeredByService

import app.main.service.match_conditions as mc


api = MatchDto.api


@api.route('/studies')
class MatchStudies(Resource):
    def get(self):
        all_studies = StudyService.get_all(Study)
        all_study_links = StudyLinksService.get_all(StudyLinks)

        try:                
            if all_studies:
                studies = [x.as_dict() for x in all_studies]
                study_links = [x.as_dict() for x in all_study_links]
                
                body=[]
                for study in studies:
                    if study.get('active'):
                        data = {
                            'id': study.get('id'),
                            'title': study.get('name'),
                            'description': study.get('description'),
                            'locations': []
                        }

                        the_links = list(filter(lambda x: x['study_id'] == study.get('id'), study_links))

                        links = []
                        for link in the_links:
                            L = {
                                'name': link.get('name'),
                                'href': link.get('href')
                            }
                            links.append(L)
                        data.update({'links': links})
                        
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
        all_el_criteria_has_criterion = ElCriteriaHasCriterionService.get_all(ElCriteriaHasCriterion)
        all_value = ValueService.get_all(Value)

        all_criterion = CriterionService.get_all(Criterion)
        all_input_type = InputTypeService.get_all(InputType)

        try:
            if all_el_criteria_has_criterion:
                body = []
                
                el_criteria_has_criterion = [x.as_dict() for x in all_el_criteria_has_criterion]
                value = [x.as_dict() for x in all_value]

                criterion = [x.as_dict() for x in all_criterion]
                input_type = [x.as_dict() for x in all_input_type]
                
                
                for echc in el_criteria_has_criterion:
                    if mc.is_active(echc):

                        the_id = echc.get('id')
                        fieldId = echc.get('criterion_id')

                        value_id = echc.get('value_id')
                        the_value = list(filter(lambda x: x['id'] == value_id, value))[0]
                        operator = the_value.get('operator')

                        #choose fieldValue as value or value_id, depending on input_type
                        crit = list(filter(lambda x: x['id'] == fieldId, criterion))[0]
                        input_type_id = crit.get('input_type_id')
                        it = list(filter(lambda x: x['id'] == input_type_id, input_type))[0]
                        render_type = it.get('render_type')
                        if render_type in ['radio', 'select']:
                            fieldValue = value_id
                        elif render_type in ['age']:
                            unit = the_value.get('unit')
                            if unit in ['years']:
                                fieldValue = eval(the_value.get('value_string'))
                            else:
                                if unit in ['months']:
                                    fieldValue = round(eval(the_value.get('value_string'))/12.0)
                                elif unit in ['days']:
                                    fieldValue = round(eval(the_value.get('value_string'))/365.0)
                        else:
                            fieldValue = eval(the_value.get('value_string'))


                        f = {
                            'id': the_id,
                            'fieldId': fieldId,
                            'fieldValue': fieldValue,
                            'operator': operator
                        }
                        body.append(f)
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


@api.route('/match-form')
class MatchMatchForm(Resource):
    def get(self):
        all_tags = TagService.get_all(Tag)
        try:
            if all_tags:
                #get groups
                tags = [x.as_dict() for x in all_tags]
                G = mc.groups(tags)

                all_display_rules = DisplayRulesService.get_all(DisplayRules)
                all_input_type = InputTypeService.get_all(InputType)
                all_criterion = CriterionService.get_all(Criterion)
                all_criterion_has_tag = CriterionHasTagService.get_all(CriterionHasTag)
                all_criterion_has_value = CriterionHasValueService.get_all(CriterionHasValue)
                all_value = ValueService.get_all(Value)
                all_triggered_by = TriggeredByService.get_all(TriggeredBy)
                
                display_rules = [x.as_dict() for x in all_display_rules]
                input_type = [x.as_dict() for x in all_input_type]
                criterion = [x.as_dict() for x in all_criterion]
                criterion_has_tag = [x.as_dict() for x in all_criterion_has_tag]
                criterion_has_value = [x.as_dict() for x in all_criterion_has_value]
                value = [x.as_dict() for x in all_value]
                triggered_by = [x.as_dict() for x in all_triggered_by]

                F = mc.form(
                    display_rules,
                    input_type,
                    criterion,
                    criterion_has_tag,
                    criterion_has_value,
                    value,
                    triggered_by
                )

                body = {"groups": G, "fields": F}
                
                return jsonify(
                    {
                        "current_date": date.today().strftime("%B %d, %Y"),
                        "current_time": strftime("%H:%M:%S +0000", gmtime()),
                        "status": "OK",
                        "body": body
                    }
                )
            else:
                body = []
        except:
            api.abort(404, message="error: problem with data or form calculator")
        
