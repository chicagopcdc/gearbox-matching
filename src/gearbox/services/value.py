from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import exc 
from fastapi import HTTPException
from gearbox.schemas import ValueCreate, ValueSearchResults, Value as ValueSchema
from gearbox.util import status
from gearbox.crud import value_crud, unit_crud

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

"""
async def build_new_value(value_str: str, operator: str, unit: str, is_numeric: bool) -> ValueCreate:
    # build code and description from input and return ValueCreate schema
    if is_numeric:
        unit_abrv = None
        match unit:
            case: "days" or "months" or "years"
        code = operator + '_' + value_str + '_' + 

    return ValueCreate()
"""