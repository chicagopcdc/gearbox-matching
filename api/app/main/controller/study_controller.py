from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
from time import gmtime, strftime
import json

from app.main.util.dto import StudyDto
from app.main.util import AlchemyEncoder
from app.main.service.study_service import get_all_studies, get_a_study, get_study_version

api = StudyDto.api
_study = StudyDto.study



@api.route('/<public_id>')
@api.param('public_id', 'The Study identifier')
@api.response(404, 'Study not found.')
class Study(Resource):
    @api.doc('get a study')
    @api.marshal_with(_study)
    def get(self, public_id):
        study = get_a_study(public_id)
        if not study:
            api.abort(404)
        else:
            return study.as_dict()


@api.route('/info')
class info(Resource):
    def get(self):
        studies = get_all_studies() 

        return jsonify({
            "current_date": date.today().strftime("%B %d, %Y"),
            "current_time": strftime("%H:%M:%S +0000", gmtime()),
            "status": "OK",
            "body": [r.as_dict() for r in studies]
        })
