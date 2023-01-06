import datetime
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import CriterionHasTag
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..util import status

from cdislogging import get_logger
logger = get_logger(__name__)

async def add_criterion_has_tag(current_session: Session, data: dict):

    new_criterion_has_tag = CriterionHasTag(criterion_id=data.criterion_id,
        tag_id=data.tag_id
        )
    current_session.add(new_criterion_has_tag)
    try:
        await current_session.commit()
        return new_criterion_has_tag
    except IntegrityError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, f"INTEGRITY SQL ERROR: {type(e)}: {e}")
    except exc.SQLAlchemyError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")