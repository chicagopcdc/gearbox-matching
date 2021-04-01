import uuid
import datetime

from app.main import DbSession
from app.main.model.study_links import StudyLinks
from app.main.service import Services

class StudyLinksService(Services):
    
    def save_new_study_links(self, data):
        study_links = self.get_a_study_links(self, data.get('id'))

        if not study_links:
            new_study_links = StudyLinks(
                study_id=data.get('study_id'),
                name=data.get('name'),
                href=data.get('href'),
                active=data.get('active')
            )
            Services.save_changes(new_study_links)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'StudyLinks already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_study_links(self, id):
        return DbSession.query(StudyLinks).filter(StudyLinks.id==id).first()
