import uuid
import datetime

from app.main import DbSession
from app.main.model.login import Login

def save_new_user(data):
    user = DbSession.query(Login).filter(Login.id==data['id']).first()
    
    if not user:
        new_user = Login(
            id=data['id'],
            refresh_token=data['refresh_token'],
            iat=data['iat'],
            exp=data['exp'],
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists.',
        }
        return response_object, 409

def get_all_users():
    return DbSession.query(Login).all()
    
def get_a_user(id):
    return DbSession.query(Login).filter(Login.id==id).first()

def save_changes(users_obj):
    DbSession.add(users_obj)
    DbSession.commit()

def user_commit():
    DbSession.commit()
