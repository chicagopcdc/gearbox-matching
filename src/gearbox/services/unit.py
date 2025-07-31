import json
from datetime import datetime

from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import exc
from fastapi import HTTPException
from gearbox.models import Unit
from gearbox.schemas import UnitCreate, UnitSearchResults, Unit as UnitSchema
from gearbox.util import status, json_utils
from gearbox.crud import unit_crud

async def get_unit(session: Session, id: int) -> UnitSchema:
    unit = await unit_crud.get(session, id)
    return unit

async def get_unit(session: Session, name: str) -> UnitSchema:
    unit = await unit_crud.get_unit(session, name)
    return unit

async def get_units(session: Session) -> UnitSearchResults:
    unit = await unit_crud.get_multi(session)
    return unit
    pass

async def create_unit(session: Session, unit: UnitCreate) -> UnitSchema:

    new_unit = await unit_crud.create(db=session, obj_in=unit)
    return new_unit

async def update_unit(session: Session, unit: UnitCreate, unit_id: int):
    unit_in = await unit_crud.get(db=session, id=unit_id)
    if unit_in:
        await unit_crud.update(db=session, db_obj=unit_in, obj_in=unit)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unit for id: {unit_id} not found for update.") 

