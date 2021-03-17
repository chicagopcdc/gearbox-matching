import datetime

from app.main import DbSession
from app.main.model.criterion_has_value import CriterionHasValue
from app.main.service import Services

class CriterionHasValueService(Services):

    def save_new_criterion_has_value(self, data):
        criterion_has_value = self.get_a_criterion_has_value(self, data.get('criterion_id'))

        if not criterion_has_value:
            new_criterion_has_value = CriterionHasValue(
                value_id=data.get('value_id'),
                criterion_id=data.get('criterion_id'),
                create_date=datetime.datetime.utcnow(),
            )
            Services.save_changes(new_criterion_has_value)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'CriterionHasValue already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_criterion_has_value(self, criterion_id):
        return DbSession.query(CriterionHasValue).filter(
            CriterionHasValue.criterion_id==criterion_id,
        ).first()
