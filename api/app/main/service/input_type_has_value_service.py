import datetime

from app.main import DbSession
from app.main.model.input_type_has_value import InputTypeHasValue
from app.main.service import Services

class InputTypeHasValueService(Services):

    def save_new_input_type_has_value(self, data):
        input_type_has_value = self.get_a_input_type_has_value(self, data.get('criterion_id'))

        if not input_type_has_value:
            new_input_type_has_value = InputTypeHasValue(
                value_id=data.get('value_id'),
                criterion_id=data.get('criterion_id'),
                create_date=datetime.datetime.utcnow(),
            )
            Services.save_changes(new_input_type_has_value)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'InputTypeHasValue already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_input_type_has_value(self, criterion_id):
        return DbSession.query(InputTypeHasValue).filter(
            InputTypeHasValue.criterion_id==criterion_id,
        ).first()
