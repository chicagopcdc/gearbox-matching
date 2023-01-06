import datetime
from sqlalchemy import update, select, exc
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import InputType
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..util import status

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_all_input_types(current_session: Session):
    stmt = select(InputType)
    result = await current_session.execute(stmt)
    input_types = result.scalars().all()
    return input_types

async def add_input_type(current_session: Session, data: dict):

    new_input_type = InputType(data_type=data.data_type,
        render_type=data.render_type,
        create_date=datetime.datetime.utcnow(),
        )
    current_session.add(new_input_type)
    try:
        await current_session.commit()
        return new_input_type
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Unique constraint ERROR: data_type: {data.data_type} render_type: {data.render_type} already exists.")
    except exc.SQLAlchemyError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")