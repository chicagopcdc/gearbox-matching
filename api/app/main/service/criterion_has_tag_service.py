import uuid
import datetime

from app.main import DbSession
from app.main.model.criterion_has_tag import CriterionHasTag
from app.main.service import Services

class CriterionHasTagService(Services):

    def save_new_criterion_has_tag(self, data):
        criterion_has_tag = self.get_a_criterion_has_tag(self, data.get('criterion_id'))

        if not criterion_has_tag:
            new_criterion_has_tag = CriterionHasTag(
                criterion_id=data.get('criterion_id'),
                tag_id=data.get('tag_id'),
            )
            Services.save_changes(new_criterion_has_tag)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'CriterionHasTag already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_criterion_has_tag(self, criterion_id):
        return DbSession.query(CriterionHasTag).filter(
            CriterionHasTag.criterion_id==criterion_id
        ).first()

