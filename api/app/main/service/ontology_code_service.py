import uuid
import datetime

from app.main import DbSession
from app.main.model.ontology_code import OntologyCode
from app.main.service import Services

class OntologyCodeService(Services):

    def save_new_ontology_code(data):
        ontology_code = DbSession.query(OntologyCode).filter(OntologyCode.code==data.get('code')).first()

        if not ontology_code:
            new_ontology_code = OntologyCode(
                id=data.get('id'),
                ontology_url=data.get('ontology_url'),
                name=data.get('name'),
                code=data.get('code'),
                value=data.get('value'),
                version=data.get('version')
            )
            Services.save_changes(new_ontology_code)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'OntologyCode already exists. Please Log in.',
            }
            return response_object, 409

    def get_a_ontology_code(code):
        return DbSession.query(OntologyCode).filter(OntologyCode.code==code).first()

