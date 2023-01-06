from sqlalchemy import update, select, exc
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import TriggeredBy
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..util import status

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_all_triggered_by(current_session: Session):
    stmt = select(TriggeredBy)
    result = await current_session.execute(stmt)
    triggered_bys= result.scalars().all()
    return triggered_bys

async def add_triggered_by(current_session: Session, data: dict):

    new_triggered_by= TriggeredBy(display_rules_id=data.display_rules_id,
        criterion_id=data.criterion_id,
        value_id=data.value_id,
        path=data.path,
        active=True,
        version=data.version
        )
    current_session.add(new_triggered_by)
    try:
        await current_session.commit()
        return new_triggered_by
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Unique constraint ERROR: display_rules_id: {data.display_rules_id} criterion_id: {data.criterion_id} value_id: {data.value_id} path: {data.path} already exists.")
    except exc.SQLAlchemyError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")

