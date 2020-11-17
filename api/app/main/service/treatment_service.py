import uuid
import datetime

from app.main import DbSession
from app.main.model.treatment import Treatment
from app.main.service import Services

class TreatmentService(Services):

    def save_new_treatment(data):
        try:
            treatment = DbSession.query(Treatment).filter(Treatment.level_code==data['level_code']).first()
        except:
            treatment=None

        if not treatment:
            new_treatment = Treatment(
                id = data.get('id'),
                level_code=data.get('level_code'),
                level_display=data.get('level_display'),
                description=data.get('description'),
                create_date=datetime.datetime.utcnow(),
                active=data.get('active'),
            )
            Services.save_changes(new_treatment)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Treatment already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_treatment(level_code):
        return DbSession.query(Treatment).filter(Treatment.level_code==level_code).first()

    # def get_treatment_version(id):
    #     return DbSession.query(TreatmentVersion).filter(TreatmentVersion.id==id).first()

