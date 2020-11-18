import uuid
import datetime

from app.main import DbSession
from app.main.model.arm_treatment import ArmTreatment
from app.main.service import Services

class ArmTreatmentService(Services):

    def save_new_arm_treatment(data):
        arm_treatment = DbSession.query(ArmTreatment).filter(
            ArmTreatment.arm_id==data.get('arm_id'),
            ArmTreatment.treatment_id==data.get('treatment_id'),
        ).first()

        if not arm_treatment:
            new_arm_treatment = ArmTreatment(
                arm_id=data.get('arm_id'),
                treatment_id=data.get('treatment_id'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active'),
            )
            Services.save_changes(new_arm_treatment)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'ArmTreatment already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_arm_treatment(data):
        return DbSession.query(ArmTreatment).filter(
            ArmTreatment.arm_id==data['arm_id'],
            ArmTreatment.treatment_id==data['treatment_id']
        ).first()
    
    # def get_arm_treatment_version(id):
    #     return DbSession.query(ArmTreatmentVersion).filter(ArmTreatmentVersion.id==id).first()

