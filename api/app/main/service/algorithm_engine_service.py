import uuid
import datetime

from app.main import DbSession
from app.main.model.algorithm_engine import AlgorithmEngine
from app.main.service import Services

class AlgorithmEngineService(Services):

    def save_new_algorithm_engine(data):
        algorithm_engine = DbSession.query(AlgorithmEngine).filter(AlgorithmEngine.name==data.get('name')).first()

        if not algorithm_engine:
            new_algorithm_engine = AlgorithmEngine(
                version=data.get('version'),
                name=data.get('name'),
                link=data.get('link'),
                description=data.get('description'),
                function=data.get('function'),
                type=data.get('type'),
            )
                    
            Services.save_changes(new_algorithm_engine)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'AlgorithmEngine already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_algorithm_engine(public_id):
        return DbSession.query(AlgorithmEngine).filter(AlgorithmEngine.id==public_id).first()

    def get_algorithm_engine_version(id):
        return DbSession.query(AlgorithmEngineVersion).filter(AlgorithmEngineVersion.id==id).first()

