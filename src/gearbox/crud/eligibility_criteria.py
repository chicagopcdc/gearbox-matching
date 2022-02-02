from re import I
from telnetlib import EL
from sqlalchemy import func, update, select, exc
from .. import logger
from sqlalchemy.orm import Session, joinedload
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import ElCriteriaHasCriterion

async def get_eligibility_criteria(current_session: Session):
    stmt = select(ElCriteriaHasCriterion).options(
        joinedload(ElCriteriaHasCriterion.criterion),
        joinedload(ElCriteriaHasCriterion.value),
        joinedload(ElCriteriaHasCriterion.eligibility_criteria)
    )
    result = await current_session.execute(stmt)
    sites = result.unique().scalars().all()
    return sites