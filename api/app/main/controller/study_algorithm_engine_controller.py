from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.study_algorithm_engine import StudyAlgorithmEngine
from app.main.service.study_algorithm_engine_service import StudyAlgorithmEngineService
from app.main.util import AlchemyEncoder
from app.main.util.dto import StudyAlgorithmEngineDto


api = StudyAlgorithmEngineDto.api
_study_algorithm_engine = StudyAlgorithmEngineDto.study_algorithm_engine


@api.route('')
class StudyAlgorithmEngineInfo(Resource):
    @api.doc('get a study_algorithm_engine')
    @api.marshal_with(_study_algorithm_engine)
    def get(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        study_algorithm_engine = StudyAlgorithmEngineService.get_a_study_algorithm_engine(self, data)
        if not study_algorithm_engine:
            api.abort(404, message="study_algorithm_engine '{}' not found".format(data))
        else:
            return study_algorithm_engine.as_dict()


@api.route('/info')
class AllStudyAlgorithmEnginesInfo(Resource):
    def get(self):
        study_algorithm_engines = StudyAlgorithmEngineService.get_all(StudyAlgorithmEngine)
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
        template = StudyAlgorithmEngine()
        allowed_keys = template.as_dict().keys()
        
        new_study_algorithm_engine_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_study_algorithm_engine_dict.update({key:data[key]})
        try:
            response = StudyAlgorithmEngineService.save_new_study_algorithm_engine(StudyAlgorithmEngineService, new_study_algorithm_engine_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/delete_study_algorithm_engine')
class Delete(Resource):
    @api.doc('delete a study_algorithm_engine')
    def delete(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")        
        study_algorithm_engine = StudyAlgorithmEngineService.get_a_study_algorithm_engine(self, data)
        if not study_algorithm_engine:
            api.abort(404, message="study_algorithm_engine '{}' not found".format(data))

        try:
            StudyAlgorithmEngineService.delete(study_algorithm_engine)
            return study_algorithm_engine.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
