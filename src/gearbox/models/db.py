from .. import config

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = config.DB_STRING
SQLALCHEMY_ALEMBIC_DATABASE_URI = config.ALEMBIC_DB_STRING


engine = create_async_engine(SQLALCHEMY_DATABASE_URI, future=True, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)