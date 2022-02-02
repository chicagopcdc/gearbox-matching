import datetime
from re import I
from sqlalchemy import func, update, select, exc
from .. import logger
from sqlalchemy.orm import Session

from gearbox.models.models import AlgorithmEngine

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

async def get_match_conditions(current_session: Session):

    stmt = select(AlgorithmEngine)

    result = await current_session.execute(stmt)
    ae = result.scalars().all()
    return ae
