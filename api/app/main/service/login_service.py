import uuid
import datetime

from app.main import DbSession
from app.main.model.login import Login

def save_new_login(data):
    login = DbSession.query(Login).filter(Login.sub_id==data['sub_id']).first()
    
    if not login:
        new_login = Login(
            sub_id=data['sub_id'],
            refresh_token=data['refresh_token'],
            iat=data['iat'],
            exp=data['exp'],
        )
        save_changes(new_login)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User Login already exists.',
        }
        return response_object, 409

def get_all_logins():
    return DbSession.query(Login).all()
    
def get_a_login(sub_id):
    return DbSession.query(Login).filter(Login.sub_id==sub_id).first()

def save_changes(login_obj):
    DbSession.add(login_obj)
    DbSession.commit()

def login_commit():
    DbSession.commit()

def login_delete(login_obj):
    DbSession.delete(login_obj)
    DbSession.commit()
