import datetime
from re import I
from sqlalchemy import select, exc, subquery
from typing import Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session 
from gearbox.models import StudyVersion
from gearbox.util.types import StudyVersionStatus

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_study_versions(session: Session)->List[StudyVersion]:

    stmt = select(StudyVersion).where(StudyVersion.active==True)
    result = await session.execute(stmt)
    ae = result.unique().scalars().all()

    return ae