from re import I
from telnetlib import EL
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session, joinedload, join
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import ElCriteriaHasCriterion, Criterion, InputType

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_eligibility_criteria_info(current_session: Session):

    stmt = select(ElCriteriaHasCriterion).options(
        joinedload(ElCriteriaHasCriterion.criterion).options(
            joinedload(Criterion.input_type)
        ),
        joinedload(ElCriteriaHasCriterion.value)
    ).order_by(ElCriteriaHasCriterion.id)

    result = await current_session.execute(stmt)
    ec = result.unique().scalars().all()
    return ec
