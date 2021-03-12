from app.main import DbSession
from app.main.model.triggered_by import TriggeredBy
from app.main.service import Services

class TriggeredByService(Services):

    def save_new_triggered_by(self, data):
        triggered_by = self.get_a_triggered_by(self, data.get('criterion_id'))

        if not triggered_by:
            new_triggered_by = TriggeredBy(
                display_rules_id=data.get('display_rules_id'),
                criterion_id=data.get('criterion_id'),
                value_id=data.get('value_id'),
                path=data.get('path'),
            )
            Services.save_changes(new_triggered_by)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'TriggeredBy already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_triggered_by(self, criterion_id):
        return DbSession.query(TriggeredBy).filter(
            TriggeredBy.criterion_id==criterion_id,
        ).first()
