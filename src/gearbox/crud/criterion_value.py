import datetime
from re import I
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session

from gearbox.models.models import Value

from fastapi import HTTPException
from asyncpg import UniqueViolationError
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_values(current_session: Session):

    stmt = select(Value)

    result = await current_session.execute(stmt)
    ae = result.scalars().all()
    return ae
