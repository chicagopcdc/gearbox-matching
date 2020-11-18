import uuid
import datetime

from app.main import DbSession
from app.main.model.xyz import Xyz
from app.main.service import Services

class XyzService(Services):

    def save_new_xyz(data):
        xyz = DbSession.query(Xyz).filter(Xyz.code==data.get('code')).first()

        if not xyz:
            new_xyz = Xyz(
                name=data.get('name'),
                code=data.get('code'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active'),
            )
            Services.save_changes(new_xyz)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Xyz already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_xyz(code):
        return DbSession.query(Xyz).filter(Xyz.code==code).first()

    def get_xyz_version(id):
        return DbSession.query(XyzVersion).filter(XyzVersion.id==id).first()

