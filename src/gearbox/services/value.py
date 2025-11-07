from . import logger
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import exc 
from fastapi import HTTPException
from gearboxdatamodel.schemas import ValueCreate, ValueSearchResults, Value as ValueSchema
from gearboxdatamodel.util import status
from gearboxdatamodel.crud import value_crud, unit_crud
from gearboxdatamodel.schemas import ValueCreate, UnitCreate, ValueSave
from gearboxdatamodel.models import Value
from typing import List

async def get_value(session: Session, id: int) -> ValueSchema:
    aes = await value_crud.get(session, id)
    return aes

async def get_value_by_value_string(session: Session, value_string: str) -> ValueSchema:
    val = await value_crud.get_value_by_value_string(session, value_string)
    return val

async def get_values(session: Session, ids: List[int] = []) -> ValueSearchResults:
    if not ids:
        aes = await value_crud.get_multi(session)
    else:
        query_ids =  ','.join(str(id) for id in ids)
        aes = await value_crud.get_multi(session, where=[f"{Value.__table__.name}.id in ({query_ids})"])
    return aes

async def create_value(session: Session, value: ValueCreate) -> ValueSchema:

    # if value is not numeric validate against existing values
    if not value.is_numeric:
        dup_val = await get_value_by_value_string(session=session, value_string=value.value_string)
        if dup_val:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Error creating value-string {value.value_string} already exists.")

    # if no unit_id, then find it or create it
    if not value.unit_id:
        unit = await unit_crud.get_unit(session, value.unit_name)
        if not unit:
            unit_create = UnitCreate(name=value.unit_name)
            unit = await unit_crud.create(db=session, obj_in=unit_create)
            # add returned unit.id to the new value
        value.unit_id = unit.id
    value_ins = ValueSave(
            description=value.description,
            is_numeric=value.is_numeric,
            value_string=value.value_string,
            unit_id=value.unit_id,
            operator=value.operator,
            active=value.active
    )
    new_value = await value_crud.create(db=session, obj_in=value_ins)
    await session.commit() 
    return new_value

async def update_value(session: Session, value: ValueSchema) -> ValueSchema:
    value_in = await value_crud.get(db=session, id=value.id)

    # if not-numeric and the value-string has changed, validate 
    # to ensure a duplicate value-string is not being created in the update
    if not value_in.is_numeric and value_in.value_string != value.value_string:
        existing_value = get_value_by_value_string(session=session, value_string=value_in.value_string)
        if existing_value.id != value_in.id:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Error value-string {value_in.value_string} already exists with id = {existing_value.id}.")

    if value_in:
        upd_value = await value_crud.update(db=session, db_obj=value_in, obj_in=value)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Value for id: {value.id} not found for update.") 
    await session.commit() 
    return upd_value

async def get_value_id(session: Session, value_str: str, operator: str, unit: str, is_numeric: bool) -> int:
    # check if value exists
    # if not, then create one
    value = await value_crud.get_value(db=session, value_str=value_str, operator=operator, unit_name=unit, is_numeric=is_numeric)
    if not value:
        value_cr = ValueCreate(description=value_str, 
                            value_string=value_str,
                            unit_name=unit,
                            operator=operator,
                            is_numeric=is_numeric, 
                            active=True)
        value = await create_value(session=session, value=value_cr)

    return value.id
