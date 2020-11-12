import uuid
import datetime

from app.main import DbSession
from app.main.model.study_algorithm_engine import Study_Algorithm_Engine
from app.main.service import Services


class Study_Algorithm_EngineService(Services):

    def save_new_study_algorithm_engine(data):
        #NOT DRY
        study_algorithm_engine = DbSession.query(Study_Algorithm_Engine).filter(
            Study_Algorithm_Engine.study_version_id==data['study_version_id'],
            Study_Algorithm_Engine.algorithm_engine_id==data['algorithm_engine_id'],
            Study_Algorithm_Engine.study_id==data['study_id'],
        ).first()

        if not study_algorithm_engine:
            new_study_algorithm_engine = Study_Algorithm_Engine(
                study_version_id=data.get('study_version_id'),
                algorithm_engine_id=data.get('algorithm_engine_id'),
                study_id=data.get('study_id'),                
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
                'message': 'Study_Algorithm_Engine already exists. Please Log in.',
            }
            return response_object, 409


    def get_a_study_algorithm_engine(data):
        return DbSession.query(Study_Algorithm_Engine).filter(
            Study_Algorithm_Engine.study_version_id==data['study_version_id'],
            Study_Algorithm_Engine.algorithm_engine_id==data['algorithm_engine_id'],
            Study_Algorithm_Engine.study_id==data['study_id'],
        ).first()
