import uuid
import datetime

from app.main import DbSession
from app.main.model.study_version import StudyVersion

def save_new_study_version(data):
    study_version = DbSession.query(StudyVersion).filter(StudyVersion.id==data['id']).first()

    if not study_version:
        new_study_version = StudyVersion(
            id = data['id'],
            study_id=data['study_id'],
            create_date=datetime.datetime.utcnow(),
            active=data['active']
        )
        save_changes(new_study_version)
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

def get_all_study_versions():
    return DbSession.query(StudyVersion).all()

def get_a_study_version(id):
    return DbSession.query(StudyVersion).filter(StudyVersion.id==id).first()

def save_changes(study_version_obj):
    DbSession.add(study_version_obj)
    DbSession.commit()
    
def study_version_commit():
    DbSession.commit()
    
def study_version_delete(study_version_obj):
    DbSession.delete(study_version_obj)
    DbSession.commit()
