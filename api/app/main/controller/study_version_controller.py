from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.study_version import StudyVersion
from app.main.service.study_version_service import StudyVersionService
from app.main.util import AlchemyEncoder
from app.main.util.dto import StudyVersionDto


api = StudyVersionDto.api
_study_version = StudyVersionDto.study_version


@api.route('/<public_id>')
@api.param('public_id', 'The Study identifier')
class StudyVersionInfo(Resource):
    @api.doc('get a study_version')
    @api.marshal_with(_study_version)
    def get(self, public_id):
        study = StudyVersionService.get_a_study_version(self, public_id)
        if not study:
            api.abort(404, message="study '{}' not found".format(public_id))
        else:
            return study.as_dict()


@api.route('/info')
class AllStudyVersionsInfo(Resource):
    def get(self):
        study_versions = StudyVersionService.get_all(StudyVersion)
        try:
            if study_versions:
                body = [r.as_dict() for r in study_versions]
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
            api.abort(404, message="study_version table not found or has no data")


@api.route('/create_study_version')
class Create(Resource):
    @api.doc('create a new study_version')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = StudyVersion()
        allowed_keys = template.as_dict().keys()

        new_study_version_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_study_version_dict.update({key:data[key]})
        try:
            response = StudyVersionService.save_new_study_version(StudyVersionService, new_study_version_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_study_version/<public_id>')
@api.param('public_id', 'The StudyVersion identifier')
class Update(Resource):
    @api.doc('update an existing study_version')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the study_version to be updated
        study_version = StudyVersionService.get_a_study_version(self, public_id)
        if not study_version:
            api.abort(404, message="study_version '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = study_version.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='study_id':
                    existing_study_version_with_new_code = StudyVersionService.get_a_study_version(self, data[key])
                    if not existing_study_version_with_new_code:
                        setattr(study_version, key, data[key])
                    else:
                        #code values must be unique for each study_version
                        api.abort(409, message="study_version code '{}' is duplicate".format(data[key]))
                else:
                    setattr(study_version, key, data[key])
        try:
            StudyVersionService.commit()
            return study_version.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_study_version/<public_id>')
@api.param('public_id', 'The StudyVersion identifier')
class Delete(Resource):
    @api.doc('delete a study_version')
    def delete(self, public_id):
        study_version = StudyVersionService.get_a_study_version(self, public_id)
        if not study_version:
            api.abort(404, message="study_version '{}' not found".format(public_id))

        try:
            StudyVersionService.delete(study_version)
            return study_version.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
