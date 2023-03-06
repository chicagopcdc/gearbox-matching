import datetime
from re import I
from sqlalchemy import func, update, select, exc
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from gearbox.schemas.algorithm_engine import AlgorithmResponse
from sqlalchemy.orm import Session, joinedload 

from gearbox.models import StudyAlgorithmEngine, StudyVersion

from cdislogging import get_logger
logger = get_logger(__name__)


async def get_study_algorithm_engines(session: Session)->List[StudyAlgorithmEngine]:

    stmt = select(StudyAlgorithmEngine).options(
        joinedload(StudyAlgorithmEngine.study_version)
    ).filter(StudyVersion.active == True).filter(StudyAlgorithmEngine.active == True)

    result = await session.execute(stmt)
    ae = result.unique().scalars().all()

    return ae