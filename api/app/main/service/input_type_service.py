import uuid
import datetime

from app.main import DbSession
from app.main.model.input_type import InputType
from app.main.service import Services

class InputTypeService(Services):

    def save_new_input_type(self, data):
        input_type = self.get_a_input_type(self, data.get('id'))

        if not input_type:
            new_input_type = InputType(
                data_type=data.get('data_type'),
                render_type=data.get('render_type'),
                create_date=datetime.datetime.utcnow()
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

    def get_a_input_type(self, id):
        return DbSession.query(InputType).filter(InputType.id==id).first()