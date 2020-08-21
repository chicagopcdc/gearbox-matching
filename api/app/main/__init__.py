from flask import Flask, _app_ctx_stack
from flask_cors import CORS
# from flask_bcrypt import Bcrypt
from flask_sqlalchemy import BaseQuery, SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .config import config_by_name


# database session registry object, configured from
# create_app factory
DbSession = scoped_session(
    sessionmaker(),
    # __ident_func__ should be hashable, therefore used
    # for recognizing different incoming requests
    scopefunc=_app_ctx_stack.__ident_func__
)


def create_app(name_handler, config_object):
    """
    Application factory

    :param name_handler: name of the application.
    :param config_object: the configuration object.
    """
    app = Flask(name_handler)
    app.config.from_object(config_by_name[config_object])
    app.engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

    #allow cross-origin-resource-sharing (CORS), e.g. frontend at port:3000
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    
    global DbSession
    # BaseQuery class provides some additional methods like
    # first_or_404() or get_or_404() -- borrowed from
    # mitsuhiko's Flask-SQLAlchemy
    DbSession.configure(bind=app.engine, query_cls=BaseQuery)

    @app.teardown_appcontext
    def teardown(exception=None):
        global DbSession
        if DbSession:
            DbSession.remove()

    return app
