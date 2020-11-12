from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.study_algorithm_engine import Study_Algorithm_Engine
from app.main.service.study_algorithm_engine_service import Study_Algorithm_EngineService
from app.main.util import AlchemyEncoder
from app.main.util.dto import StudyAlgorithmEngineDto


api = StudyAlgorithmEngineDto.api
_study_algorithm_engine = StudyAlgorithmEngineDto.study_algorithm_engine


@api.route('/<public_id>')
@api.param('public_id', 'The Study_Algorithm_Engine identifier')
class Study_Algorithm_EngineInfo(Resource):
    @api.doc('get a study_algorithm_engine')
    @api.marshal_with(_study_algorithm_engine)
    def get(self, public_id):
        pid = public_id.split('-')
        data = {
            'study_version_id': pid[0],
            'algorithm_engine_id': pid[1],
            'study_id': pid[2]
        }
        study_algorithm_engine = Study_Algorithm_EngineService.get_a_study_algorithm_engine(data)
        if not study_algorithm_engine:
            api.abort(404, message="study_algorithm_engine '{}' not found".format(public_id))
        else:
            return study_algorithm_engine.as_dict()


@api.route('/info')
class AllStudy_Algorithm_EnginesInfo(Resource):
    def get(self):
        study_algorithm_engines = Study_Algorithm_EngineService.get_all(Study_Algorithm_Engine)
        try:
            if study_algorithm_engines:
                body = [r.as_dict() for r in study_algorithm_engines]
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
            api.abort(404, message="study_algorithm_engine table not found or has no data")


@api.route('/create_study_algorithm_engine')
class Create(Resource):
    @api.doc('create a new study_algorithm_engine')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = Study_Algorithm_Engine()
        allowed_keys = template.as_dict().keys()
        
        new_study_algorithm_engine_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_study_algorithm_engine_dict.update({key:data[key]})
        try:
            response = Study_Algorithm_EngineService.save_new_study_algorithm_engine(new_study_algorithm_engine_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_study_algorithm_engine/<public_id>')
@api.param('public_id', 'The Study_Algorithm_Engine identifier')
class Update(Resource):
    @api.doc('update an existing study_algorithm_engine')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the study_algorithm_engine to be updated
        pid = public_id.split('-')
        pid_data = {
            'study_version_id': pid[0],
            'algorithm_engine_id': pid[1],
            'study_id': pid[2]
        }
        study_algorithm_engine = Study_Algorithm_EngineService.get_a_study_algorithm_engine(pid_data)
        if not study_algorithm_engine:
            api.abort(404, message="study_algorithm_engine '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = study_algorithm_engine.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                #DO NOT PREVENT PRIMARY KEY CHANGES
                setattr(study_algorithm_engine, key, data[key])
        try:
            Study_Algorithm_EngineService.commit()
            return study_algorithm_engine.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_study_algorithm_engine/<public_id>')
@api.param('public_id', 'The Study_Algorithm_Engine identifier')
class Delete(Resource):
    @api.doc('delete a study_algorithm_engine')
    def delete(self, public_id):
        pid = public_id.split('-')
        pid_data = {
            'study_version_id': pid[0],
            'algorithm_engine_id': pid[1],
            'study_id': pid[2]
        }
        study_algorithm_engine = Study_Algorithm_EngineService.get_a_study_algorithm_engine(pid_data)
        if not study_algorithm_engine:
            api.abort(404, message="study_algorithm_engine '{}' not found".format(public_id))

        try:
            Study_Algorithm_EngineService.delete(study_algorithm_engine)
            return study_algorithm_engine.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
