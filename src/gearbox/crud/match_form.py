from re import I
from telnetlib import EL
from sqlalchemy import func, update, select, exc
from fastapi import HTTPException
from gearbox.util import status

from gearbox.models.criterion_has_tag import CriterionHasTag
from sqlalchemy.orm import Session, joinedload, join, noload
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models import DisplayRules, TriggeredBy, Criterion, CriterionHasTag, Value

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_form_info(current_session: Session):

    stmt = select(DisplayRules).options(
        joinedload(DisplayRules.triggered_bys).options(
            joinedload(TriggeredBy.criterion).options(
                noload(Criterion.el_criteria_has_criterions),
            ),
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

async def clear_display_rules_and_triggered_by(current_session: Session):
    try:
        await current_session.execute('DELETE FROM triggered_by')
        await current_session.execute('DELETE FROM display_rules')
        await current_session.commit()
    except exc.SQLAlchemyError as e:
        logger.error(f"Error clearing triggered_by and display_rules tables: {type(e)}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")


async def insert_display_rules(current_session: Session, display_rules_rows: list):
    mylist = [{
        "id": i.get('id'), 
        "criterion_id": i.get('criterion_id'),
        "priority": i.get('priority'),
        "active": i.get('active'),
        "version": i.get('version')
        } for i in display_rules_rows
    ]
    try:
        await current_session.execute(
            DisplayRules.__table__.insert(), mylist
        )
    except exc.SQLAlchemyError as e:
        logger.error(f"Error inserting display_rules: {type(e)}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")

    await current_session.commit()

async def insert_triggered_by(current_session: Session, triggered_by_rows: list):
    mylist = [{
        "id": i.get('id'), 
        "display_rules_id": i.get('display_rules_id'),
        "criterion_id": i.get('criterion_id'),
        "value_id": i.get('value_id'),
        "path": i.get('path'),
        "active": i.get('active')
        } for i in triggered_by_rows
    ]
    try:
        await current_session.execute(
            TriggeredBy.__table__.insert(), mylist
        )
    except exc.SQLAlchemyError as e:
        logger.error(f"Error inserting triggered_by: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")

    await current_session.commit()