import datetime
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import CriterionHasValue
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..util import status

from cdislogging import get_logger
logger = get_logger(__name__)

async def add_criterion_has_value(current_session: Session, data: dict):

    new_criterion_has_value = CriterionHasValue(criterion_id=data.criterion_id,
        value_id=data.value_id,
        assoc_create_date=datetime.datetime.utcnow()
        )
    current_session.add(new_criterion_has_value)
    try:
        await current_session.commit()
        return new_criterion_has_value
    except IntegrityError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, f"INTEGRITY SQL ERROR: {type(e)}: {e}")
    except exc.SQLAlchemyError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")