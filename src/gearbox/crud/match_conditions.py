import datetime
from re import I
from sqlalchemy import select, exc
from typing import Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session 
from gearbox.models import EligibilityCriteriaInfo
from gearbox.util.types import EligibilityCriteriaInfoStatus

from cdislogging import get_logger
logger = get_logger(__name__)


async def get_study_algorithm_engines(session: Session)->List[EligibilityCriteriaInfo]:

    stmt = select(EligibilityCriteriaInfo).filter(EligibilityCriteriaInfo.status == EligibilityCriteriaInfoStatus.ACTIVE.value)
    result = await session.execute(stmt)
    ae = result.unique().scalars().all()

    return ae