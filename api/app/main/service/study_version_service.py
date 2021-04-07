import uuid
import datetime

from app.main import DbSession
from app.main.model.study_version import StudyVersion
from app.main.service import Services

class StudyVersionService(Services):
    
    def save_new_study_version(self, data):
        study_version = self.get_a_study_version(self, data.get('study_id'))

        if not study_version:
            new_study_version = StudyVersion(
                study_id=data.get('study_id'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active')
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

    def get_a_study_version(self, study_id):
        return DbSession.query(StudyVersion).filter(StudyVersion.study_id==study_id).first()

