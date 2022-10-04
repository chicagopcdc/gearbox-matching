import datetime
from re import I
from sqlalchemy import func, update, select, exc

from gearbox.schemas.algorithm_engine import AlgorithmResponse
from sqlalchemy.orm import Session, joinedload

from gearbox.models.models import AlgorithmEngine, StudyAlgorithmEngine

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

async def get_algorithm_engines(current_session: Session):

    stmt = select(AlgorithmEngine).options(
        joinedload(AlgorithmEngine.study_algo_engine).options(
            joinedload(StudyAlgorithmEngine.study_version)
        )
    ).order_by(AlgorithmEngine.sequence)
    result = await current_session.execute(stmt)
    ae = result.unique().scalars().all()
    return ae
