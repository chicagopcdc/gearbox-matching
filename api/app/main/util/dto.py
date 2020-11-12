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


class LoginDto:
    api = Namespace('login', description='OICD login POST relay')
    login = api.model('login', {
        'sub_id': fields.String(required=True, description="sub_id from fence /user"),
        'refresh_token': fields.String(required=True, description="oicd token"),
        'iat': fields.String(required=True, description="issued at time"),
        'exp': fields.String(required=True, description="expires at time"),
    })

###################################################
###################################################

class XyzDto:
    api = Namespace('xyz', description='xyz related operations')
    xyz = api.model('xyz', {
    	'id': fields.String(required=True, description="xyz id"),
        'name': fields.String(required=True, description='xyz name'),
        'code': fields.String(required=True, description='xyz code'),
        'create_date': fields.String(required=True, description='xyz creation time'),
        'active': fields.String(description='is xyz active')
    })    

class StudyVersionDto:
    api = Namespace('study_version', description='study_version related operations')
    study_version = api.model('study_version', {
    	'id': fields.String(required=True, description="study_version id"),
        'study_id': fields.String(required=True, description='study id'),
        'create_date': fields.String(required=True, description='study_version creation time'),
        'active': fields.String(description='is study_version active')
    })    

class StudyAlgorithmEngineDto:
    api = Namespace('study_algorithm_engine', description='study_algorithm_engine related operations')
    study_algorithm_engine = api.model('study_algorithm_engine', {
    	'study_version_id': fields.String(required=True, description="study_version id"),
        'algorithm_engine_id': fields.String(required=True, description='algorithm_engine id'),
        'study_id': fields.String(required=True, description='study id'),
        'start_date': fields.String(description='start date'),
        'active': fields.String(description='is study_algorithm_engine active')
    })

class AlgorithmEngineDto:
    api = Namespace('algorithm_engine', description='algorithm_engine related operations')
    algorithm_engine = api.model('algorithm_engine', {
    	'id': fields.String(required=True, description="algorithm_engine id"),
        'version': fields.String(description='algorithm_engine version'),
        'name': fields.String(description='algorithm_engine name'),
        'link': fields.String(description='algorithm_engine link'),
        'description': fields.String(description='algorithm_engine description'),
        'function': fields.String(description='algorithm_engine function'),
        'type': fields.String(description='algorithm_engine type')
    })
