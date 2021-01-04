import uuid
import datetime

from app.main import DbSession
from app.main.model.tag import Tag
from app.main.service import Services

class TagService(Services):

    def save_new_tag(data):
        tag = DbSession.query(Tag).filter(Tag.code==data.get('code')).first()

        if not tag:
            new_tag = Tag(
                id=data.get('id'),
                code=data.get('code'),
                type=data.get('type'),
            )
            Services.save_changes(new_tag)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Tag already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_tag(code):
        return DbSession.query(Tag).filter(Tag.code==code).first()

