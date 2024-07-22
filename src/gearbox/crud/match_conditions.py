import datetime
from re import I
from sqlalchemy import select, exc, subquery
from typing import Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session 
from gearbox.models import EligibilityCriteriaInfo, StudyVersion
from gearbox.util.types import EligibilityCriteriaInfoStatus

from cdislogging import get_logger
logger = get_logger(__name__)


async def get_study_algorithm_engines(session: Session)->List[EligibilityCriteriaInfo]:

    sv_subq = select(StudyVersion).where(StudyVersion.active==True).subquery()
    stmt = select(EligibilityCriteriaInfo).filter(EligibilityCriteriaInfo.status == EligibilityCriteriaInfoStatus.ACTIVE.value).join(sv_subq, EligibilityCriteriaInfo.study_version_id == sv_subq.c.id)
    result = await session.execute(stmt)
    ae = result.unique().scalars().all()

    return ae
