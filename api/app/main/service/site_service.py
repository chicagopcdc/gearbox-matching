import uuid
import datetime

from app.main import DbSession
from app.main.model.site import Site
from app.main.service import Services

class SiteService(Services):

    def save_new_site(data):
        site = DbSession.query(Site).filter(Site.code==data['code']).first()

        if not site:
            new_site = Site(
                name=data.get('name'),
                code=data.get('code'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active')
            )
            Services.save_changes(new_site)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Site already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_site(code):
        return DbSession.query(Site).filter(Site.code==code).first()

    def get_site_version(id):
        return DbSession.query(SiteVersion).filter(SiteVersion.id==id).first()


