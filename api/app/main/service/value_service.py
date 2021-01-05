import uuid
import datetime

from app.main import DbSession
from app.main.model.value import Value
from app.main.service import Services

class ValueService(Services):

    def save_new_value(data):
        value = DbSession.query(Value).filter(Value.code==data.get('code')).first()

        if not value:
            new_value = Value(
                id=data.get('id'),
                code=data.get('code'),
                type=data.get('type'),
                value_string=data.get('value_string'),
                upper_threshold=data.get('upper_threshold'),
                lower_threshold=data.get('lower_threshold'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active'),
                value_list=data.get('value_list'),
                value_bool=data.get('value_bool'),
            )
            Services.save_changes(new_value)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Value already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_value(code):
        return DbSession.query(Value).filter(Value.code==code).first()

