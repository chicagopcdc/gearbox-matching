import datetime
from re import I
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import Criterion, CriterionHasValue, CriterionHasTag, DisplayRules, TriggeredBy
from fastapi import HTTPException
from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from ..util import status

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_all_criteria(current_session: Session):
    stmt = select(Criterion)
    result = await current_session.execute(stmt)
    criteria = result.unique().scalars().all()
    return criteria

async def add_criterion(current_session: Session, data: dict):

    new_criterion = Criterion(code=data.code,
        display_name=data.display_name,
        description=data.description,
        create_date=datetime.datetime.utcnow(),
        active=data.active,
        ontology_code_id=data.ontology_code_id,
        input_type_id=data.input_type_id
        # value_id
        # tag_id
        # display_rules.priority
        # display_rules.version
        )
    current_session.add(new_criterion)

    """
     FOR UPDATE TRY THIS: 
     current_session.excute(
       update(Criterion),
        [
            {"id": 1, "display_name": "NEW DISPLAY NAME"}
        ],
     )
    """
    try:
        await current_session.commit()
        new_criterion_id = new_criterion.id



        # TO DO: new crud for criterion_has_value, criterion_has_tag
        return new_criterion
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Unique constraint ERROR: code: {data.code} display_name: {data.display_name} description: {data.description} ontology_code_id: {data.ontology_code_id} input_type_id: {data.input_type_id} already exists.")
    except exc.SQLAlchemyError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")
    # INSERT criterion_has_value
    # INSERT criterion_has_tag
    # INSERT display_rules
    # INSERT triggered_by (if exists)