from re import I
from telnetlib import EL
from sqlalchemy import func, update, select, exc

from gearbox.models.criterion_has_tag import CriterionHasTag
from .. import logger
from sqlalchemy.orm import Session, joinedload, join, noload
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import DisplayRules, TriggeredBy, Criterion, CriterionHasTag

async def get_form_info(current_session: Session):

    stmt = select(DisplayRules).options(
        joinedload(DisplayRules.triggered_bys),
        joinedload(DisplayRules.criterion).options(
            joinedload(Criterion.tags).options(
                joinedload(CriterionHasTag.tag)
            ),
            joinedload(Criterion.input_type),
            noload('el_criteria_has_criterions')
        )
    ).order_by(DisplayRules.priority).limit(10)

    result = await current_session.execute(stmt)
    sites = result.unique().scalars().all()
    return sites
