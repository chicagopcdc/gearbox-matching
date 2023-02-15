import json
from datetime import datetime

from . import logger
from sqlalchemy.orm import Session
from sqlalchemy import select, exc, update
from fastapi import HTTPException
from gearbox.models import Value
from gearbox.schemas import ValueCreate, ValueSearchResults, Value as ValueSchema
from sqlalchemy.sql.functions import func
from gearbox.util import status, json_utils
from gearbox.crud import value_crud

async def get_value(session: Session, id: int) -> ValueSchema:
    aes = await value_crud.get(session, id)
    return aes

async def get_values(session: Session) -> ValueSearchResults:
    aes = await value_crud.get_multi(session)
    return aes
    pass

async def create_value(session: Session, value: ValueCreate) -> ValueSchema:
    new_value = await value_crud.create(db=session, obj_in=value)
    await session.commit() 
    return new_value

async def update_value(session: Session, value: ValueCreate, value_id: int) -> ValueSchema:
    value_in = await value_crud.get(db=session, id=value_id)
    if value_in:
        upd_value = await value_crud.update(db=session, db_obj=value_in, obj_in=value)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Value for id: {value_id} not found for update.") 
    await session.commit() 
    return upd_value

