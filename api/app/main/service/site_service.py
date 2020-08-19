import uuid
import datetime

from app.main import DbSession
from app.main.model.site import Site

def save_new_site(data):
    site = DbSession.query(Site).filter(Site.code==data['code']).first()
    
    if not site:
        new_site = Site(
            name=data['name'],
            code=data['code'],
            create_date=datetime.datetime.utcnow(),
            active=data['active']
        )
        save_changes(new_site)
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

def get_all_sites():
    return DbSession.query(Site).all()

def get_a_site(code):
    return DbSession.query(Site).filter(Site.code==code).first()

def get_site_version(id):
    return DbSession.query(SiteVersion).filter(SiteVersion.id==id).first()
    
def save_changes(site_obj):
    DbSession.add(site_obj)
    DbSession.commit()
    
def site_commit():
    DbSession.commit()
    
def site_delete(site_obj):
    DbSession.delete(site_obj)
    DbSession.commit()

