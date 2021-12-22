from .. import config

# from gino.ext.starlette import Gino
# db = Gino(
#     dsn=config.DB_DSN,
#     pool_min_size=config.DB_POOL_MIN_SIZE,
#     pool_max_size=config.DB_POOL_MAX_SIZE,
#     echo=config.DB_ECHO,
#     ssl=config.DB_SSL,
#     use_connection_for_request=config.DB_USE_CONNECTION_FOR_REQUEST,
#     retry_limit=config.DB_RETRY_LIMIT,
#     retry_interval=config.DB_RETRY_INTERVAL,
# )



# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = config.DB_STRING
SQLALCHEMY_ALEMBIC_DATABASE_URI = config.ALEMBIC_DB_STRING


# engine = create_engine(
#     SQLALCHEMY_DATABASE_URI,
#     # required for sqlite
#     # connect_args={"check_same_thread": False},
# )

engine = create_async_engine(SQLALCHEMY_DATABASE_URI, future=True, echo=True)

# engine = create_async_engine(
#         "postgresql+asyncpg://scott:tiger@localhost/test", echo=True,
#     )

# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)