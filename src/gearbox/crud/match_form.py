from re import I
from telnetlib import EL
from sqlalchemy import func, update, select, exc

from gearbox.models.criterion_has_tag import CriterionHasTag
from sqlalchemy.orm import Session, joinedload, join, noload
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import DisplayRules, TriggeredBy, Criterion, CriterionHasTag, Value

import logging
logger = logging.getLogger('gb-logger')

async def get_form_info(current_session: Session):

    stmt = select(DisplayRules).options(
        joinedload(DisplayRules.triggered_bys).options(
            joinedload(TriggeredBy.criterion).options(
                noload(Criterion.el_criteria_has_criterions),
                # noload(Criterion.input_type),
                # noload(Criterion.values),
                # noload(Criterion.tags)
            ),
            # A D D noload el_criteria_has_criterions and criterion_has_tags 
            # and criterion_has_value and input_type!!!
            joinedload(TriggeredBy.value).options(
                noload(Value.criteria),
                noload(Value.el_criteria_has_criterions)
            )
        ),
        joinedload(DisplayRules.criterion).options(
            joinedload(Criterion.tags).options(
                joinedload(CriterionHasTag.tag)
            ),
            joinedload(Criterion.input_type),
            noload('el_criteria_has_criterions')
        )
    ).order_by(DisplayRules.priority)

    result = await current_session.execute(stmt)
    sites = result.unique().scalars().all()
    return sites