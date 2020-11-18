import uuid
import datetime

from app.main import DbSession
from app.main.model.arm import Arm
from app.main.service import Services

class ArmService(Services):

    def save_new_arm(data):
        arm = DbSession.query(Arm).filter(Arm.code==data.get('code')).first()

        if not arm:
            new_arm = Arm(
                id = data.get('id'),
                version_id=data.get('version_id'),
                study_id=data.get('study_id'),
                code=data.get('code'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active'),
            )
            Services.save_changes(new_arm)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Arm already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_arm(code):
        return DbSession.query(Arm).filter(Arm.code==code).first()

    def get_arm_version(id):
        return DbSession.query(ArmVersion).filter(ArmVersion.id==id).first()

