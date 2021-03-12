from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.display_rules import DisplayRules
from app.main.service.display_rules_service import DisplayRulesService
from app.main.util import AlchemyEncoder
from app.main.util.dto import DisplayRulesDto


api = DisplayRulesDto.api
_display_rules = DisplayRulesDto.display_rules


@api.route('/<public_id>')
@api.param('public_id', 'The DisplayRules identifier')
class DisplayRulesInfo(Resource):
    @api.doc('get a display_rules')
    @api.marshal_with(_display_rules)
    def get(self, public_id):
        display_rules = DisplayRulesService.get_a_display_rules(self, public_id)
        if not display_rules:
            api.abort(404, message="display_rules '{}' not found".format(public_id))
        else:
            return display_rules.as_dict()


@api.route('/info')
class AllDisplayRulessInfo(Resource):
    def get(self):
        display_ruless = DisplayRulesService.get_all(DisplayRules)
        try:
            if display_ruless:
                body = [r.as_dict() for r in display_ruless]
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
            api.abort(404, message="display_rules table not found or has no data")


@api.route('/create_display_rules')
class Create(Resource):
    @api.doc('create a new display_rules')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = DisplayRules()
        allowed_keys = template.as_dict().keys()

        new_display_rules_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_display_rules_dict.update({key:data[key]})
        try:
            response = DisplayRulesService.save_new_display_rules(DisplayRulesService, new_display_rules_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_display_rules/<public_id>')
@api.param('public_id', 'The DisplayRules identifier')
class Update(Resource):
    @api.doc('update an existing display_rules')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the display_rules to be updated
        display_rules = DisplayRulesService.get_a_display_rules(self, public_id)
        if not display_rules:
            api.abort(404, message="display_rules '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = display_rules.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                #DO NOT PREVENT PRIMARY KEY CHANGES
                setattr(display_rules, key, data[key])
        try:
            DisplayRulesService.commit()
            return display_rules.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_display_rules/<public_id>')
@api.param('public_id', 'The DisplayRules identifier')
class Delete(Resource):
    @api.doc('delete a display_rules')
    def delete(self, public_id):
        display_rules = DisplayRulesService.get_a_display_rules(self, public_id)
        if not display_rules:
            api.abort(404, message="display_rules '{}' not found".format(public_id))

        try:
            DisplayRulesService.delete(display_rules)
            return display_rules.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
