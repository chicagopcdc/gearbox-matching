import datetime
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import Value
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..util import status

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_all_values(current_session: Session):
    # stmt = select(Value).where(Value.active==True)
    stmt = select(Value)
    result = await current_session.execute(stmt)
    values = result.scalars().all()
    return values

async def add_value(current_session: Session, data: dict):

    new_value = Value(code=data.code,
        description=data.description,
        type=data.type,
        value_string=data.value_string,
        unit=data.unit,
        operator=data.operator,
        create_date=datetime.datetime.utcnow(),
        active=data.active
        )
    logger.info(f"-----------------------------> NEW VALUE CODE: {data.code}")
    current_session.add(new_value)
    try:
        await current_session.commit()
        return new_value
    except IntegrityError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, f"INTEGRITY SQL ERROR: {type(e)}: {e}")
    except exc.SQLAlchemyError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")