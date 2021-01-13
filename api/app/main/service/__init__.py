import uuid
import datetime

from app.main import DbSession

class Services:
    
    def get_all(model_object):
        return DbSession.query(model_object).all()

    def save_changes(model_object):
        DbSession.add(model_object)
        DbSession.commit()

    def commit():
        DbSession.commit()

    def delete(model_object):
        DbSession.delete(model_object)
        DbSession.commit()
