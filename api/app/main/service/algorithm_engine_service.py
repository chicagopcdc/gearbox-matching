import uuid
import datetime

from app.main import DbSession
from app.main.model.algorithm_engine import AlgorithmEngine
from app.main.service import Services

class AlgorithmEngineService(Services):

    def save_new_algorithm_engine(self, data):
        algorithm_engine = self.get_a_algorithm_engine(self, data)

        if not algorithm_engine:
            new_algorithm_engine = AlgorithmEngine(
                id=data.get('id'),
                el_criteria_has_criterion_id=data.get('el_criteria_has_criterion_id'),
                parent_id=data.get('parent_id'),
                parent_path=data.get('parent_path'),
                operator=data.get('operator'),
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

    def get_a_algorithm_engine(self, data):
        return DbSession.query(AlgorithmEngine).filter(
            AlgorithmEngine.pk==data.get('pk'),
            AlgorithmEngine.id==data.get('id'),
        ).first()


