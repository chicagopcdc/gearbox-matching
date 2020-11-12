import uuid
import datetime

from app.main import DbSession
from app.main.model.study import Study
from app.main.model.study_version import StudyVersion
from app.main.service import Services

class StudyService(Services):
    
    def save_new_study(data):
        study = DbSession.query(Study).filter(Study.code==data['code']).first()

        if not study:
            new_study = Study(
                name=data.get('name'),
                code=data.get('code'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active')
            )
            Services.save_changes(new_study)
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


    def get_a_study(code):
        return DbSession.query(Study).filter(Study.code==code).first()

    def get_study_version(id):
        return DbSession.query(StudyVersion).filter(StudyVersion.id==id).first()
