import uuid
import datetime

from app.main import DbSession
from app.main.model.login import Login
from app.main.service import Services

class LoginService(Services):

    def save_new_login(data):
        login = DbSession.query(Login).filter(Login.sub_id==data['sub_id']).first()

        if not login:
            new_login = Login(
                sub_id=data.get('sub_id'),
                refresh_token=data.get('refresh_token'),
                iat=data.get('iat'),
                exp=data.get('exp'),
            )
            Services.save_changes(new_login)
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

    def get_a_login(sub_id):
        return DbSession.query(Login).filter(Login.sub_id==sub_id).first()

