import uuid
import datetime

from app.main import DbSession
from app.main.model.criterion_has_value import CriterionHasValue
from app.main.service import Services

class CriterionHasValueService(Services):

    def save_new_criterion_has_value(data):
        criterion_has_value = DbSession.query(CriterionHasValue).filter(
            CriterionHasValue.value_id==data.get('value_id'),
            CriterionHasValue.criterion_id==data.get('criterion_id')
        ).first()

        if not criterion_has_value:
            new_criterion_has_value = CriterionHasValue(
                value_id=data.get('value_id'),
                criterion_id=data.get('criterion_id'),
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

    def get_a_criterion_has_value(data):
        return DbSession.query(CriterionHasValue).filter(
            CriterionHasValue.value_id==data.get('value_id'),
            CriterionHasValue.criterion_id==data.get('criterion_id'),
        ).first()

    # def get_a_criterion_has_value(code):
    #     return DbSession.query(CriterionHasValue).filter(CriterionHasValue.code==code).first()

