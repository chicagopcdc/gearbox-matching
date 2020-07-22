import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@mysql-development:3306/pedal_dev_v_0"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ERROR_404_HELP = False #<-supresses default flask (unhelpful) 404 help message

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test')) #<-put the sqlite3 db file in test dir

    SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    #DEBUG
    #SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite://' #<- in memory db

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ERROR_404_HELP = False #<-supresses default flask (unhelpful) 404 help message

class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
