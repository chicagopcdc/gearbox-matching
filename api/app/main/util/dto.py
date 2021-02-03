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
        'start_date': fields.String(description='start date'),
        'active': fields.String(description='is study_algorithm_engine active')
    })

class AlgorithmEngineDto:
    api = Namespace('algorithm_engine', description='algorithm_engine related operations')
    algorithm_engine = api.model('algorithm_engine', {
    	'id': fields.String(required=True, description="algorithm_engine id"),
    	'el_criteria_has_criterion_id': fields.String(description="algorithm_engine el_criteria_has_criterion_id"),
    	'parent_id': fields.String(description="algorithm_engine parent_id"),
        'parent_path': fields.String(description="algorithm_engine parent_path"),
    	'operator': fields.String(description="algorithm_engine operator")
    })


class EligibilityCriteriaDto:
    api = Namespace('eligibility_criteria', description='eligibility_criteria related operations')
    eligibility_criteria = api.model('eligibility_criteria', {
    	'id': fields.String(required=True, description="eligibility_criteria id"),
        'create_date': fields.String(description='eligibility_criteria create_date'),
        'active': fields.String(description='is eligibility_criteria active'),
        'study_version_id': fields.String(required=True, description='eligibility_criteria study_version_id')
    })


class CriterionDto:
    api = Namespace('criterion', description='criterion related operations')
    criterion = api.model('criterion', {
    	'id': fields.String(required=True, description="criterion id"),
        'code': fields.String(description='criterion code'),
        'display_name': fields.String(description='criterion display_name'),
        'description': fields.String(description='criterion description'),
        'create_date': fields.String(description='criterion create_date'),
        'active': fields.String(description='is criterion active'),
        'ontology_code_id': fields.String(description='criterion ontology_code_id'),
        'input_type_id': fields.String(description='criterion input_type_id')
    })


class TagDto:
    api = Namespace('tag', description='tag related operations')
    tag = api.model('tag', {
    	'id': fields.String(required=True, description="tag id"),
        'code': fields.String(description='tag code'),
        'type': fields.String(description='tag type')
    })


class CriterionHasTagDto:
    api = Namespace('criterion_has_tag', description='criterion_has_tag related operations')
    criterion_has_tag = api.model('criterion_has_tag', {
    	'criterion_id': fields.String(required=True, description="criterion_has_tag criterion_id"),
    	'tag_id': fields.String(required=True, description="criterion_has_tag tag_id")
    })


class ElCriteriaHasCriterionDto:
    api = Namespace('el_criteria_has_criterion', description='el_criteria_has_criterion related operations')
    el_criteria_has_criterion = api.model('el_criteria_has_criterion', {
        'id': fields.String(required=True, description="el_criteria_has_criterion id"),
    	'criterion_id': fields.String(required=True, description="el_criteria_has_criterion criterion_id"),
        'eligibility_criteria_id': fields.String(required=True, description='el_criteria_has_criterion eligibility_criteria_id'),
        'create_date': fields.String(description='el_criteria_has_criterion create_date'),
        'active': fields.String(description='is el_criteria_has_criterion active'),
        'value_id': fields.String(description='el_criteria_has_criterion value_id')
    })


class ValueDto:
    api = Namespace('value', description='value related operations')
    value = api.model('value', {
    	'id': fields.String(required=True, description="value id"),
    	'code': fields.String(description="value code"),
    	'type': fields.String(description="value type"),
    	'value_string': fields.String(description="value value_string"),
    	'upper_threshold': fields.String(description="value upper_threshold"),
    	'lower_threshold': fields.String(description="value lower_threshold"),
    	'create_date': fields.String(description="value create_date"),
    	'active': fields.String(description="value active"),
    	'value_list': fields.String(description="value value_list"),
    	'value_bool': fields.String(description="value value_bool"),  
    	'upper_modifier': fields.String(description="value upper_modifier"),
    	'lower_modifier': fields.String(description="value lower_modifier")
    })

    
class EligibilityCriteriaHasNoteDto:
    api = Namespace('eligibility_criteria_has_note', description='eligibility_criteria_has_note related operations')
    eligibility_criteria_has_note = api.model('eligibility_criteria_has_note', {
        'eligibility_criteria_id': fields.String(required=True, description='eligibility_criteria_has_note eligibility_criteria_id'),
        'note_id': fields.String(required=True, description='eligibility_criteria_has_note note_id')
    })


class NoteDto:
    api = Namespace('note', description='note related operations')
    note = api.model('note', {
    	'id': fields.String(required=True, description="note id"),
        'value': fields.String(description='note value')
    })

    
class InputTypeDto:
    api = Namespace('input_type', description='input_type related operations')
    input_type = api.model('input_type', {
    	'id': fields.String(required=True, description="input_type id"),
        'type': fields.String(description='input_type type'),
        'name': fields.String(description='input_type code')
    })


class OntologyCodeDto:
    api = Namespace('ontology_code', description='ontology_code related operations')
    ontology_code = api.model('ontology_code', {
    	'id': fields.String(required=True, description="ontology_code id"),
    	'ontology_url': fields.String(description="ontology_code ontology_url"),
    	'name': fields.String(description="ontology_code name"),
    	'code': fields.String(description="ontology_code code"),
    	'value': fields.String(description="ontology_code value"),
    	'version': fields.String(description="ontology_code version")
    })
