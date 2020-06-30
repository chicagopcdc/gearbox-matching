from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.util.dto import StudyDto
from app.main.util import AlchemyEncoder
from app.main.service.study_service import get_all_studies, get_a_study, get_study_version, save_new_study

from app.main.model.study import Study


api = StudyDto.api
_study = StudyDto.study


@api.route('/<public_id>')
@api.param('public_id', 'The Study identifier')
@api.response(404, 'Study not found.')
#class Study(Resource):
class StudyInfo(Resource):
    @api.doc('get a study')
    @api.marshal_with(_study)
    def get(self, public_id):
        study = get_a_study(public_id)
        if not study:
            api.abort(404)
        else:
            return study.as_dict()


@api.route('/info')
#class info(Resource):
class AllStudiesInfo(Resource):
    def get(self):
        studies = get_all_studies() 

        return jsonify({
            "current_date": date.today().strftime("%B %d, %Y"),
            "current_time": strftime("%H:%M:%S +0000", gmtime()),
            "status": "OK",
            "body": [r.as_dict() for r in studies]
        })


@api.route('/new_study')
class Create(Resource):
    @api.doc('create a new study')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = Study()
        allowed_keys = template.as_dict().keys()

        new_study_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_study_dict.update({key:data[key]})
        try:
            save_new_study(new_study_dict)
            return new_study_dict
        except Exception as e:
            logging.error(e, exc_info=True)
