from flask_restplus import Namespace, fields


class XyzDto:
    api = Namespace('xyz', description='xyz related operations')
    xyz = api.model('xyz', {
    	'id': fields.String(required=True, description="xyz id"),
        'name': fields.String(required=True, description='xyz name'),
        'code': fields.String(required=True, description='xyz code'),
        'create_date': fields.String(required=True, description='xyz creation time'),
        'active': fields.String(description='is xyz active')
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


class LoginDto:
    api = Namespace('login', description='OICD login POST relay')
    login = api.model('login', {
        'sub_id': fields.String(required=True, description="sub_id from fence /user"),
        'refresh_token': fields.String(required=True, description="oicd token"),
        'iat': fields.String(required=True, description="issued at time"),
        'exp': fields.String(required=True, description="expires at time"),
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

class ArmDto:
    api = Namespace('arm', description='arm related operations')
    arm = api.model('arm', {
    	'id': fields.String(required=True, description="arm id"),
        'version_id': fields.String(description='arm version_id'),
        'study_id': fields.String(description='arm study_id'),
        'code': fields.String(description='arm code'),
        'create_date': fields.String(description='arm create_date'),
        'active': fields.String(description='is arm active')
    })


class TreatmentDto:
    api = Namespace('treatment', description='treatment related operations')
    treatment = api.model('treatment', {
    	'id': fields.String(required=True, description="treatment id"),
        'level_code': fields.String(description='treatment level_code'),
        'level_display': fields.String(description='treatment level_display'),
        'description': fields.String(description='treatment description'),
        'create_date': fields.String(description='treatment create_date'),
        'active': fields.String(description='is treatment active')
    })

    
class ArmTreatmentDto:
    api = Namespace('arm_treatment', description='arm_treatment related operations')
    arm_treatment = api.model('arm_treatment', {
    	'arm_id': fields.String(required=True, description="arm_treatment arm_id"),
        'treatment_id': fields.String(description='arm_treatment treatment_id'),
        'create_date': fields.String(description='arm_treatment create_date'),
        'active': fields.String(description='is arm_treatment active')
    })


class EligibilityCriteriaDto:
    api = Namespace('eligibility_criteria', description='eligibility_criteria related operations')
    eligibility_criteria = api.model('eligibility_criteria', {
    	'id': fields.String(required=True, description="eligibility_criteria id"),
        'arm_id': fields.String(description='eligibility_criteria arm_id'),
        'create_date': fields.String(description='eligibility_criteria create_date'),
        'active': fields.String(description='is eligibility_criteria active')
    })


class CriterionDto:
    api = Namespace('criterion', description='criterion related operations')
    criterion = api.model('criterion', {
    	'id': fields.String(required=True, description="criterion id"),
        'code': fields.String(description='criterion code'),
        'display_name': fields.String(description='criterion display_name'),
        'description': fields.String(description='criterion description'),
        'create_date': fields.String(description='criterion create_date'),
        'active': fields.String(description='is criterion active')
    })


class ValueDto:
    api = Namespace('value', description='value related operations')
    value = api.model('value', {
    	'id': fields.String(required=True, description="value id"),
        'code': fields.String(description='value coded'),
        'type': fields.String(description='value type'),
        'display_value': fields.String(description='value display_value'),
        'upper_threshold': fields.String(description='value upper_threshold'),
        'lower_threshold': fields.String(description='value lower_threshold'),
        'create_date': fields.String(description='value create_date'),
        'active': fields.String(description='is value active')
    })
