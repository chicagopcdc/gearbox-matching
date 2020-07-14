import uuid
import datetime

from app.main import db
from app.main.model.study import Study
from app.main.model.study_version import StudyVersion

def save_new_study(data):
    study = Study.query.filter_by(code=data['code']).first()                     
    if not study:
        new_study = Study(
            name=data['name'],
            code=data['code'],
            create_date=datetime.datetime.utcnow(),
            active=data['active']
        )
        save_changes(new_study)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Study already exists. Please Log in.',
        }
        return response_object, 409

def get_all_studies():
    return Study.query.all()

def get_a_study(code):
    return Study.query.filter_by(code=code).first()

def get_study_version(id):
    return StudyVersion.query.filter_by(id=id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def study_commit():
    db.session.commit()

def study_delete(data):
    db.session.delete(data)
    db.session.commit()
