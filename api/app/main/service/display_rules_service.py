from app.main import DbSession
from app.main.model.display_rules import DisplayRules
from app.main.service import Services

class DisplayRulesService(Services):

    def save_new_display_rules(self, data):
        display_rules = self.get_a_display_rules(self, data.get('id'))

        if not display_rules:
            new_display_rules = DisplayRules(
                criterion_id=data.get('criterion_id'),
                priority=data.get('priority'),
                active=data.get('active'),
                version=data.get('version'),                
            )
            Services.save_changes(new_display_rules)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'DisplayRules already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_display_rules(self, id):
        return DbSession.query(DisplayRules).filter(
            DisplayRules.id==id
        ).first()
