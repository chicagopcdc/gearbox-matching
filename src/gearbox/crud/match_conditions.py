import datetime
from re import I
from sqlalchemy import func, update, select, exc
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from gearbox.schemas.algorithm_engine import AlgorithmResponse
from sqlalchemy.orm import Session, selectinload, joinedload

from gearbox.models import StudyAlgorithmEngine, StudyVersion, EligibilityCriteriaInfo

from cdislogging import get_logger
logger = get_logger(__name__)


async def get_study_algorithm_engines(session: Session)->List[EligibilityCriteriaInfo]:

    stmt = select(EligibilityCriteriaInfo).filter(EligibilityCriteriaInfo.active == True)
    result = await session.execute(stmt)
    ae = result.unique().scalars().all()

    return ae