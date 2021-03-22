import uuid
import datetime

from app.main import DbSession
from app.main.model.value import Value
from app.main.service import Services

class ValueService(Services):

    def save_new_value(self, data):
        value = self.get_a_value(self, data.get('id'))

        if not value:
            new_value = Value(
                code=data.get('code'),
                description=data.get('description'),
                type=data.get('type'),
                value_string=data.get('value_string'),
                unit=data.get('unit'),
                operator=data.get('operator'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active'),
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

    def get_a_value(self, id):
        return DbSession.query(Value).filter(
            Value.id==id
         ).first()
