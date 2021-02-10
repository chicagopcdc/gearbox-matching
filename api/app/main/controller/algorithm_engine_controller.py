from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.algorithm_engine import AlgorithmEngine
from app.main.service.algorithm_engine_service import AlgorithmEngineService
from app.main.util import AlchemyEncoder
from app.main.util.dto import AlgorithmEngineDto


api = AlgorithmEngineDto.api
_algorithm_engine = AlgorithmEngineDto.algorithm_engine


@api.route('/<public_id>')
@api.param('public_id', 'The AlgorithmEngine identifier')
class AlgorithmEngineInfo(Resource):
    @api.doc('get a algorithm_engine')
    @api.marshal_with(_algorithm_engine)
    def get(self, public_id):
        pid = public_id.split('-')
        data = {
            'pk': pid[0],
            'id': pid[1],
        }
        algorithm_engine = AlgorithmEngineService.get_a_algorithm_engine(self, data)
        if not algorithm_engine:
            api.abort(404, message="algorithm_engine '{}' not found".format(public_id))
        else:
            return algorithm_engine.as_dict()


@api.route('/info')
class AllAlgorithmEnginesInfo(Resource):
    def get(self):
        algorithm_engines = AlgorithmEngineService.get_all(AlgorithmEngine)
        try:
            if algorithm_engines:
                body = [r.as_dict() for r in algorithm_engines]
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


@api.route('/create_algorithm_engine')
class Create(Resource):
    @api.doc('create a new algorithm_engine')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = AlgorithmEngine()
        allowed_keys = template.as_dict().keys()

        new_algorithm_engine_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_algorithm_engine_dict.update({key:data[key]})
        try:
            response = AlgorithmEngineService.save_new_algorithm_engine(AlgorithmEngineService, new_algorithm_engine_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_algorithm_engine/<public_id>')
@api.param('public_id', 'The AlgorithmEngine identifier')
class Update(Resource):
    @api.doc('update an existing algorithm_engine')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the algorithm_engine to be updated
        pid = public_id.split('-')
        pid_data = {
            'pk': pid[0],
            'id': pid[1],
        }
        algorithm_engine = AlgorithmEngineService.get_a_algorithm_engine(self, pid_data)
        if not algorithm_engine:
            api.abort(404, message="algorithm_engine '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = algorithm_engine.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='id':
                    existing_algorithm_engine_with_new_code = AlgorithmEngineService.get_a_algorithm_engine(self, data[key])
                    if not existing_algorithm_engine_with_new_code:
                        setattr(algorithm_engine, key, data[key])
                    else:
                        #code values must be unique for each algorithm_engine
                        api.abort(409, message="algorithm_engine code '{}' is duplicate".format(data[key]))
                else:
                    setattr(algorithm_engine, key, data[key])
        try:
            AlgorithmEngineService.commit()
            return algorithm_engine.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_algorithm_engine/<public_id>')
@api.param('public_id', 'The AlgorithmEngine identifier')
class Delete(Resource):
    @api.doc('delete a algorithm_engine')
    def delete(self, public_id):
        pid = public_id.split('-')
        pid_data = {
            'pk': pid[0],
            'id': pid[1],
        }
        algorithm_engine = AlgorithmEngineService.get_a_algorithm_engine(self, pid_data)
        if not algorithm_engine:
            api.abort(404, message="algorithm_engine '{}' not found".format(public_id))

        try:
            AlgorithmEngineService.delete(algorithm_engine)
            return algorithm_engine.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
