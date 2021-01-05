from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.ontology_code import OntologyCode
from app.main.service.ontology_code_service import OntologyCodeService
from app.main.util import AlchemyEncoder
from app.main.util.dto import OntologyCodeDto


api = OntologyCodeDto.api
_ontology_code = OntologyCodeDto.ontology_code


@api.route('/<public_id>')
@api.param('public_id', 'The OntologyCode identifier')
class OntologyCodeInfo(Resource):
    @api.doc('get a ontology_code')
    @api.marshal_with(_ontology_code)
    def get(self, public_id):
        ontology_code = OntologyCodeService.get_a_ontology_code(public_id)
        if not ontology_code:
            api.abort(404, message="ontology_code '{}' not found".format(public_id))
        else:
            return ontology_code.as_dict()


@api.route('/info')
class AllOntologyCodesInfo(Resource):
    def get(self):
        ontology_codes = OntologyCodeService.get_all(OntologyCode)
        try:
            if ontology_codes:
                body = [r.as_dict() for r in ontology_codes]
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
            api.abort(404, message="ontology_code table not found or has no data")


@api.route('/create_ontology_code')
class Create(Resource):
    @api.doc('create a new ontology_code')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = OntologyCode()
        allowed_keys = template.as_dict().keys()

        new_ontology_code_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_ontology_code_dict.update({key:data[key]})
        try:
            response = OntologyCodeService.save_new_ontology_code(new_ontology_code_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_ontology_code/<public_id>')
@api.param('public_id', 'The OntologyCode identifier')
class Update(Resource):
    @api.doc('update an existing ontology_code')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the ontology_code to be updated
        ontology_code = OntologyCodeService.get_a_ontology_code(public_id)
        if not ontology_code:
            api.abort(404, message="ontology_code '{}' not found".format(public_id))

        #set new key/ontology_codes
        allowed_keys = ontology_code.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='code':
                    existing_ontology_code_with_new_code = OntologyCodeService.get_a_ontology_code(data[key])
                    if not existing_ontology_code_with_new_code:
                        setattr(ontology_code, key, data[key])
                    else:
                        #code ontology_codes must be unique for each ontology_code
                        api.abort(409, message="ontology_code code '{}' is duplicate".format(data[key]))
                else:
                    setattr(ontology_code, key, data[key])
        try:
            OntologyCodeService.commit()
            return ontology_code.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_ontology_code/<public_id>')
@api.param('public_id', 'The OntologyCode identifier')
class Delete(Resource):
    @api.doc('delete a ontology_code')
    def delete(self, public_id):
        ontology_code = OntologyCodeService.get_a_ontology_code(public_id)
        if not ontology_code:
            api.abort(404, message="ontology_code '{}' not found".format(public_id))

        try:
            OntologyCodeService.delete(ontology_code)
            return ontology_code.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
