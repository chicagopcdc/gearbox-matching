from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import exc 
from fastapi import HTTPException
from gearbox.schemas import ValueCreate, ValueSearchResults, Value as ValueSchema
from gearbox.util import status
from gearbox.crud import value_crud, unit_crud
from gearbox.schemas import ValueCreate

async def get_value(session: Session, id: int) -> ValueSchema:
    aes = await value_crud.get(session, id)
    return aes

async def get_values(session: Session) -> ValueSearchResults:
    aes = await value_crud.get_multi(session)
    return aes
    pass

async def create_value(session: Session, value: ValueCreate) -> ValueSchema:
    # get unit if exists else create one
    unit = unit_crud.get_unit(value.unit_name)
    if not unit:
        unit = unit_crud.create(value.unit_name)
    # add returned unit.id to the new value
        value.unit_id = unit.id
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

async def get_value_id(value_str: str, operator: str, unit: str, is_numeric: bool) -> int:
    # check if value exists
    # if not, then create one
    value_id = value_crud.get_value(value_str=value_str, operator=operator, unit=unit, is_numeric=is_numeric)
    if not value_id:
        value = ValueCreate(description=value_str, 
                            value_str=value_str,
                            unit_name=unit,
                            operator=operator,
                            is_numeric=is_numeric)
        new_value = create_value(value)
        value_id = new_value.id
    return value_id