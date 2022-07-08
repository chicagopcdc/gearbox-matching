from re import I
from telnetlib import EL
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session, joinedload, join
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import ElCriteriaHasCriterion, Criterion, InputType

import logging
logger = logging.getLogger('gb-logger')

async def get_eligibility_criteria(current_session: Session):
#    stmt = select(ElCriteriaHasCriterion)

    stmt = select(ElCriteriaHasCriterion).options(
        joinedload(ElCriteriaHasCriterion.criterion).options(
            joinedload(Criterion.input_type)
        ),
        joinedload(ElCriteriaHasCriterion.value)
    ).order_by(ElCriteriaHasCriterion.id)

    result = await current_session.execute(stmt)
    sites = result.unique().scalars().all()
    return sites
