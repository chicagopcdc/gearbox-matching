from flask_restplus import Namespace, fields


class StudyDto:
    api = Namespace('study', description='study related operations')
    study = api.model('study', {
    	'id': fields.String(required=True, description="study id"),
        'name': fields.String(required=True, description='study name'),
        'code': fields.String(required=True, description='study code'),
        'create_date': fields.String(required=True, description='study creation time'),
        'active': fields.String(description='is study active')
    })