import uuid
import datetime

from app.main import DbSession
from app.main.model.site_has_study import SiteHasStudy
from app.main.service import Services

class SiteHasStudyService(Services):

    def save_new_site_has_study(self, data):
        site_has_study = self.get_a_site_has_study(self, data)

        if not site_has_study:
            new_site_has_study = SiteHasStudy(
                study_id=data.get('study_id'),
                site_id=data.get('site_id'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active')
            )
            Services.save_changes(new_site_has_study)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Site_Has_Study already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_site_has_study(self, data):
        return DbSession.query(SiteHasStudy).filter(
            SiteHasStudy.study_id==data.get('study_id'),
            SiteHasStudy.site_id==data.get('site_id')
        ).first()

