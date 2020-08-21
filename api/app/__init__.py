# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.study_controller import api as study_ns
from .main.controller.site_controller import api as site_ns
from .main.controller.site_has_study_controller import api as site_has_study_ns

from .main.controller.login_controller import api as login_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(study_ns, path='/study')
api.add_namespace(site_ns, path='/site')
api.add_namespace(site_has_study_ns, path='/site_has_study')

api.add_namespace(login_ns, path='/login')
