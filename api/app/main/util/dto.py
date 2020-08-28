from flask_restplus import Namespace, fields

class LoginDto:
    api = Namespace('login', description='OICD login POST relay')
    login = api.model('login', {
        #DEBUG
        #'sub_id': fields.Integer(required=True, description="sub_id from fence /user"),
        'sub_id': fields.String(required=True, description="sub_id from fence /user"),
        'refresh_token': fields.String(required=True, description="oicd token"),
        'iat': fields.String(required=True, description="issued at time"),
        'exp': fields.String(required=True, description="expires at time"),
    })

class StudyDto:
    api = Namespace('study', description='study related operations')
    study = api.model('study', {
    	'id': fields.String(required=True, description="study id"),
        'name': fields.String(required=True, description='study name'),
        'code': fields.String(required=True, description='study code'),
        'create_date': fields.String(required=True, description='study creation time'),
        'active': fields.String(description='is study active')
    })


class SiteDto:
    api = Namespace('site', description='site related operations')
    site = api.model('site', {
    	'id': fields.String(required=True, description="site id"),
        'name': fields.String(required=True, description='site name'),
        'code': fields.String(required=True, description='site code'),
        'create_date': fields.String(required=True, description='site creation time'),
        'active': fields.String(description='is site active')
    })    


class SiteHasStudyDto:
    api = Namespace('site_has_study', description='site_has_study related operations')
    site_has_study = api.model('site_has_study', {
    	'study_id': fields.String(required=True, description="study id"),
    	'site_id': fields.String(required=True, description="site id"),
        'create_date': fields.String(required=True, description='site creation time'),
        'active': fields.String(description='is site active')
    })    
