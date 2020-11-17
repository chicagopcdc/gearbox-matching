# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.study_controller import api as study_ns
from .main.controller.site_controller import api as site_ns
from .main.controller.site_has_study_controller import api as site_has_study_ns

from .main.controller.xyz_controller import api as xyz_ns
from .main.controller.study_version_controller import api as study_version_ns
from .main.controller.study_algorithm_engine_controller import api as study_algorithm_engine_ns
from .main.controller.login_controller import api as login_ns
from .main.controller.algorithm_engine_controller import api as algorithm_engine_ns
from .main.controller.arm_controller import api as arm_ns
from .main.controller.arm_treatment_controller import api as arm_treatment_ns
from .main.controller.treatment_controller import api as treatment_ns
# from .main.controller.criterion_controller import api as criterion_ns
# from .main.controller.eligibility_criteria_controller import api as eligibility_criteria_ns
# from .main.controller.el_criteria_has_criterion_controller import api as el_criteria_has_criterion_ns
# from .main.controller.value_controller import api as value_ns
# from .main.controller.criterion_has_value_controller import api as criterion_has_value_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(xyz_ns, path='/xyz')
api.add_namespace(login_ns, path='/login')
api.add_namespace(study_ns, path='/study')
api.add_namespace(site_ns, path='/site')
api.add_namespace(site_has_study_ns, path='/site_has_study')
api.add_namespace(study_version_ns, path='/study_version')
api.add_namespace(study_algorithm_engine_ns, path='/study_algorithm_engine')
api.add_namespace(algorithm_engine_ns, path='/algorithm_engine')
api.add_namespace(arm_ns, path='/arm')
api.add_namespace(arm_treatment_ns, path='/arm_treatment')
api.add_namespace(treatment_ns, path='/treatment')
# api.add_namespace(criterion_ns, path='/criterion')
# api.add_namespace(eligibility_criteria_ns, path='/eligibility_criteria')
# api.add_namespace(el_criteria_has_criterion_ns, path='/el_criteria_has_criterion')
# api.add_namespace(value_ns, path='/value')
# api.add_namespace(criterion_has_value_ns, path='/criterion_has_value')

