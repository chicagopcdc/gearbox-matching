import uuid
import datetime

from app.main import DbSession
from app.main.model.input_type import InputType
from app.main.service import Services

class InputTypeService(Services):

    def save_new_input_type(data):
        input_type = DbSession.query(InputType).filter(InputType.name==data.get('name')).first()

        if not input_type:
            new_input_type = InputType(
                id=data.get('id'),
                type=data.get('type'),
                name=data.get('name'),
            )
            Services.save_changes(new_input_type)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'InputType already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_input_type(name):
        return DbSession.query(InputType).filter(InputType.name==name).first()

