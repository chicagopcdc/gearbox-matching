from sqlalchemy import update, select, exc
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import DisplayRules
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..util import status

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_all_display_rules(current_session: Session):
    stmt = select(DisplayRules)
    result = await current_session.execute(stmt)
    display_rules = result.scalars().all()
    return display_rules

async def add_display_rule(current_session: Session, data: dict):

    new_display_rule= DisplayRules(criterion_id=data.criterion_id,
        priority=data.priority,
        active=True,
        version=data.version
        )
    current_session.add(new_display_rule)
    try:
        await current_session.commit()
        return new_display_rule
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Unique constraint ERROR: criterion_id: {data.criterion_id} priority: {data.priority} version: {data.version} already exists.")
    except exc.SQLAlchemyError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")

