from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.util.dto import StudyDto
from app.main.util import AlchemyEncoder
from app.main.service.study_service import get_all_studies, get_a_study, get_study_version, save_new_study, study_commit, study_delete

from app.main.model.study import Study


api = StudyDto.api
_study = StudyDto.study


@api.route('/<public_id>')
@api.param('public_id', 'The Study identifier')
class StudyInfo(Resource):
    @api.doc('get a study')
    @api.marshal_with(_study)
    def get(self, public_id):
        study = get_a_study(public_id)
        if not study:
            api.abort(404, message="study '{}' not found".format(public_id))
        else:
            return study.as_dict()


@api.route('/info')
class AllStudiesInfo(Resource):
    def get(self):
        studies = get_all_studies()
        try:
            if studies:
                body = [r.as_dict() for r in studies]
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


@api.route('/create_study')
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
            response = save_new_study(new_study_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_study/<public_id>')
@api.param('public_id', 'The Study identifier')
class Update(Resource):
    @api.doc('update an existing study')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the study to be updated
        study = get_a_study(public_id)
        if not study:
            api.abort(404, message="study '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = study.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='code':
                    existing_study_with_new_code = get_a_study(data[key])
                    if not existing_study_with_new_code:
                        setattr(study, key, data[key])
                    else:
                        #code values must be unique for each study
                        api.abort(409, message="study code '{}' is duplicate".format(data[key]))
                else:
                    setattr(study, key, data[key])
        try:
            study_commit()
            return study.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_study/<public_id>')
@api.param('public_id', 'The Study identifier')
class Delete(Resource):
    @api.doc('delete a study')
    def delete(self, public_id):
        study = get_a_study(public_id)
        if not study:
            api.abort(404, message="study '{}' not found".format(public_id))

        try:
            study_delete(study)
            return study.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
