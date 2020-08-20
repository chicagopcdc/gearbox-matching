import uuid
import datetime

from app.main import DbSession
from app.main.model.site import SiteHasStudy

def save_new_site_has_study(data):
    site_has_study = DbSession.query(SiteHasStudy).filter(SiteHasStudy.code==data['code']).first()
    
    if not site_has_study:
        new_site_has_study = SiteHasStudy(
            name=data['name'],
            code=data['code'],
            create_date=datetime.datetime.utcnow(),
            active=data['active']
        )
        save_changes(new_site_has_study)
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

def get_all_site_has_studies():
    return DbSession.query(SiteHasStudy).all()

def get_a_site_has_study(code):
    return DbSession.query(SiteHasStudy).filter(SiteHasStudy.code==code).first()

def get_site_has_study_version(id):
    return DbSession.query(SiteHasStudyVersion).filter(SiteHasStudyVersion.id==id).first()
    
def save_changes(site_has_study_obj):
    DbSession.add(site_has_study_obj)
    DbSession.commit()
    
def site_has_study_commit():
    DbSession.commit()
    
def site_has_study_delete(site_has_study_obj):
    DbSession.delete(site_has_study_obj)
    DbSession.commit()

