import uuid
import datetime

from app.main import DbSession
from app.main.model.study_version import StudyVersion
from app.main.service import Services

class StudyVersionService(Services):
    
    def save_new_study_version(data):
        study_version = DbSession.query(StudyVersion).filter(StudyVersion.id==data['id']).first()

        if not study_version:
            new_study_version = StudyVersion(
                id = data['id'],
                study_id=data['study_id'],
                create_date=datetime.datetime.utcnow(),
                active=data['active']
            )
            Services.save_changes(new_study_version)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'StudyVersion already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_study_version(id):
        return DbSession.query(StudyVersion).filter(StudyVersion.id==id).first()

