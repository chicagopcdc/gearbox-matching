from sqlalchemy.engine.url import make_url, URL
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from starlette.datastructures import Secret


class CommaSeparatedLogins(CommaSeparatedStrings):
    def __init__(self, value):
        super().__init__(value)
        self._items = [item.split(":") for item in self._items]

# Note:
# Configuration is in docker-compose.yml for Docker in compose services
config = Config(".env")

# Server
DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)
URL_PREFIX = config("URL_PREFIX", default="/" if DEBUG else "/gearbox")
MIDDLEWARE_URL_PREFIX = config("URL_PREFIX", default="/" if DEBUG else "/gearbox-middleware/")
BYPASS_FENCE = config("BYPASS_FENCE", cast=bool, default=False)

#S3
BYPASS_IMPORTANT_QUESTIONS = config("BYPASS_IMPORTANT_QUESTIONS", cast=bool, default=False)
BYPASS_S3 = config("BYPASS_S3", cast=bool, default=False)
# DUMMY_S3 - use a public dummy S3 bucket for docker compose testing presigned urls
DUMMY_S3 = config("DUMMY_S3", cast=bool, default=False)
S3_BUCKET_NAME = config("S3_BUCKET_NAME", default='commons-gearbox-data-bucket-with-versioning')
S3_TEST_COMPOSE_BUCKET_NAME = config("S3_TEST_COMPOSE_BUCKET_NAME", default='test-compose-gearbox-data-bucket-with-versioning')
S3_TEST_BUCKET_NAME = config("S3_TEST_BUCKET_NAME", default='test-gearbox-data-bucket-with-versioning')
S3_BUCKET_MATCH_CONDITIONS_KEY_NAME = config("S3_BUCKET_MATCH_CONDITIONS_KEY_NAME", default='match_conditions.json')
S3_BUCKET_MATCH_FORM_KEY_NAME = config("S3_BUCKET_MATCH_FORM_KEY_NAME", default='match_form.json')
S3_BUCKET_IMPORTANT_QUESTIONS_KEY_NAME = config("S3_BUCKET_IMPORTANT_QUESTIONS_KEY_NAME", default='important_questions.json')
S3_BUCKET_STUDIES_KEY_NAME = config("S3_BUCKET_STUDIES_KEY_NAME", default='gearbox_studies.json')
S3_BUCKET_ELIGIBILITY_CRITERIA_KEY_NAME = config("S3_BUCKET_ELIGIBILITY_CRITERIA_KEY_NAME", default='eligibility_criteria.json')
S3_PRESIGNED_URL_EXPIRES=config("S3_PRESIGNED_URL_EXPIRES", default="1800")
S3_PUT_OBJECT_EXPIRES=config("S3_PUT_OBJECT_EXPIRES", default="10")
S3_AWS_ACCESS_KEY_ID=config("S3_AWS_ACCESS_KEY_ID", default='')
S3_AWS_SECRET_ACCESS_KEY=config("S3_AWS_SECRET_ACCESS_KEY", default='')


# Database
# ALEMBIC DOES NOT SUPPORT ASYNC DRIVERS YET, SO WE NEED THE SYNC 
# DRIVER TO PERFORM THE MIGRATIONS
ALEMBIC_DB_DRIVER = config("DB_DRIVER", default="postgresql")
DB_DRIVER = config("DB_DRIVER", default="postgresql+asyncpg")
DB_HOST = config("DB_HOST", default=None)
DB_PORT = config("DB_PORT", cast=int, default=5432)
DB_USER = config("DB_USER", default=None)
DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default=None)
DB_DATABASE = config("DB_DATABASE", default=None)

BYPASS_FENCE_DUMMY_USER_ID = config("BYPASS_FENCE_DUMMY_USER_ID", default=4)

if TESTING:
    DB_DATABASE = "test_" + (DB_DATABASE or "gearbox")
    # DB_DATABASE = "pytest_test_" + (DB_DATABASE or "gearbox")
    DB_PORT = config("DB_PORT_TESTING", cast=int)
    TEST_KEEP_DB = config("TEST_KEEP_DB", cast=bool, default=False)
    TEST_KEEP_DB = True # KEEP TEST DATABASE AFTER TESTS
    print(f"DB DRIVER: {DB_DRIVER}")
    print(f"DB USER: {DB_USER}")
    print(f"DB PASSWORD: {DB_PASSWORD}")
    print(f"DB HOST: {DB_HOST}")
    print(f"DB PORT: {DB_PORT}")
    print(f"DB DATABASE: {DB_DATABASE}")
    print(f"BYPASS FENCE: {BYPASS_FENCE}")
    print(f"BYPASS S3: {BYPASS_S3}")
    print(f"BYPASS IMPORTANT_QUESTIONS: {BYPASS_IMPORTANT_QUESTIONS}")
    print(f"DEBUG: {DEBUG}")

DB_STRING = DB_DRIVER + "://" + DB_USER + ":" + str(DB_PASSWORD) + "@" + DB_HOST + ":" + str(DB_PORT) + "/" + DB_DATABASE
ALEMBIC_DB_STRING = ALEMBIC_DB_DRIVER + "://" + DB_USER + ":" + str(DB_PASSWORD) + "@" + DB_HOST + ":" + str(DB_PORT) + "/" + DB_DATABASE

DB_DSN = config(
    "DB_DSN",
    cast=make_url,
    default=URL.create(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE,
    ),
)

DB_MIN_SIZE = config("DB_MIN_SIZE", cast=int, default=1)  # deprecated
DB_POOL_MIN_SIZE = config("DB_POOL_MIN_SIZE", cast=int, default=DB_MIN_SIZE)
DB_MAX_SIZE = config("DB_MAX_SIZE", cast=int, default=10)  # deprecated
DB_POOL_MAX_SIZE = config("DB_POOL_MAX_SIZE", cast=int, default=DB_MAX_SIZE)
DB_ECHO = config("DB_ECHO", cast=bool, default=False)
DB_SSL = config("DB_SSL", default=None)
DB_USE_CONNECTION_FOR_REQUEST = config(
    "DB_USE_CONNECTION_FOR_REQUEST", cast=bool, default=True
)
DB_CONNECT_RETRIES = config("DB_CONNECT_RETRIES", cast=int, default=32)  # deprecated
DB_RETRY_LIMIT = config("DB_RETRY_LIMIT", cast=int, default=DB_CONNECT_RETRIES)
DB_RETRY_INTERVAL = config("DB_RETRY_INTERVAL", cast=int, default=1)


# Security
ADMIN_LOGINS = config("ADMIN_LOGINS", cast=CommaSeparatedLogins, default=[])
# option to force authutils to prioritize ALLOWED_ISSUERS setting over the issuer from
# token when redirecting, used during local docker compose setup when the
# services are on different containers but the hostname is still localhost
# When FORCE_ISSUER is set to True the ALLOWED_ISSUER must be set and contain the 
# localhost URL http://fence-service/,https://localhost/user, while USER_API should contain
# the new issuer http://fence-service/
FORCE_ISSUER = config("FORCE_ISSUER", default=None)
USER_API = config("USER_API", cast=str, default="")
ALLOWED_ISSUERS = set(config("ALLOWED_ISSUERS", cast=CommaSeparatedStrings, default=""))


# Other Services
INDEXING_SERVICE_ENDPOINT = config(
    "INDEXING_SERVICE_ENDPOINT", cast=str, default="http://indexd-service"
)
DATA_ACCESS_SERVICE_ENDPOINT = config(
    "DATA_ACCESS_SERVICE_ENDPOINT", cast=str, default="http://fence-service"
)

AWS_REGION = config("AWS_REGION", default='us-east-1')

# NEW FEATURES
ENABLE_PHI = config("ENABLE_PHI", default=False)

GEARBOX_MIDDLEWARE_PUBLIC_KEY_Path = config("GEARBOX_MIDDLEWARE_PUBLIC_KEY_PATH", default='src/gearbox/keys/jwt_public_key.pem')

GEARBOX_KEY_CONFIG = {}

# DOCCANO placeholder for new criterion
DOCCANO_MISSING_VALUE_PLACEHOLDER = config("DOCCANO_MISSING_VALUE_PLACEHOLDER", default="new_variable")
