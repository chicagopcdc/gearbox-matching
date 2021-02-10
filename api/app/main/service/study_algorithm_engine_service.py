import uuid
import datetime

from app.main import DbSession
from app.main.model.study_algorithm_engine import StudyAlgorithmEngine
from app.main.service import Services


class StudyAlgorithmEngineService(Services):

    def save_new_study_algorithm_engine(self, data):
        study_algorithm_engine = self.get_a_study_algorithm_engine(self, data)

        if not study_algorithm_engine:
            new_study_algorithm_engine = StudyAlgorithmEngine(
                study_version_id=data.get('study_version_id'),
                algorithm_engine_pk=data.get('algorithm_engine_pk'),
                algorithm_engine_id=data.get('algorithm_engine_id'),
                start_date=data.get('start_date'),
                active=data.get('active'),
            )
            Services.save_changes(new_study_algorithm_engine)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'StudyAlgorithmEngine already exists. Please Log in.',
            }
            return response_object, 409


    def get_a_study_algorithm_engine(self, data):
        return DbSession.query(StudyAlgorithmEngine).filter(
            StudyAlgorithmEngine.study_version_id==data['study_version_id'],
            StudyAlgorithmEngine.algorithm_engine_pk==data['algorithm_engine_pk'],
        ).first()
