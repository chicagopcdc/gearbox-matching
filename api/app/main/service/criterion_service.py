import uuid
import datetime

from app.main import DbSession
from app.main.model.criterion import Criterion
from app.main.service import Services

class CriterionService(Services):

    def save_new_criterion(self, data):
        criterion = self.get_a_criterion(self, data.get('code'))

        if not criterion:
            new_criterion = Criterion(
                id=data.get('id'),
                code=data.get('code'),
                display_name=data.get('display_name'),
                description=data.get('description'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active'),
                ontology_code_id=data.get('ontology_code_id'),
                input_type_id=data.get('input_type_id'),
            )
            Services.save_changes(new_criterion)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Criterion already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_criterion(self, code):
        return DbSession.query(Criterion).filter(Criterion.code==code).first()

