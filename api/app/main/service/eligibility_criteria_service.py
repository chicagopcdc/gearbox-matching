import uuid
import datetime

from app.main import DbSession
from app.main.model.eligibility_criteria import EligibilityCriteria
from app.main.service import Services

class EligibilityCriteriaService(Services):

    def save_new_eligibility_criteria(self, data):
        eligibility_criteria = self.get_a_eligibility_criteria(self, data.get('study_version_id'))

        if not eligibility_criteria:
            new_eligibility_criteria = EligibilityCriteria(
                id=data.get('id'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active'),
                study_version_id=data.get('study_version_id'),
            )
            Services.save_changes(new_eligibility_criteria)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'EligibilityCriteria already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_eligibility_criteria(self, study_version_id):
        return DbSession.query(EligibilityCriteria).filter(
            EligibilityCriteria.study_version_id==study_version_id
        ).first()