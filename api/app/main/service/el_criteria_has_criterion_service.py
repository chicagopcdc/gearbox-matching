import uuid
import datetime

from app.main import DbSession
from app.main.model.el_criteria_has_criterion import ElCriteriaHasCriterion
from app.main.service import Services

class ElCriteriaHasCriterionService(Services):

    def save_new_el_criteria_has_criterion(data):
        el_criteria_has_criterion = DbSession.query(ElCriteriaHasCriterion).filter(ElCriteriaHasCriterion.code==data.get('code')).first()

        if not el_criteria_has_criterion:
            new_el_criteria_has_criterion = ElCriteriaHasCriterion(
                criterion_id=data.get('criterion_id'),
                eligibility_criteria_id=data.get('eligibility_criteria_id'),
                arm_id=data.get('arm_id'),
                code=data.get('code'),
                display_name=data.get('display_name'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active'),
            )
            Services.save_changes(new_el_criteria_has_criterion)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'ElCriteriaHasCriterion already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_el_criteria_has_criterion(code):
        return DbSession.query(ElCriteriaHasCriterion).filter(ElCriteriaHasCriterion.code==code).first()
