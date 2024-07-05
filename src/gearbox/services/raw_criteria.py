import json
from datetime import datetime

from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import exc
from fastapi import HTTPException
from gearbox.models import RawCriteria
from gearbox.schemas import RawCriteriaCreate, RawCriteriaSearchResults, RawCriteria as RawCriteriaSchema
from gearbox.util import status, json_utils
from gearbox.crud import raw_criteria_crud
from gearbox.util.types import EligibilityCriteriaStatus

async def get_raw_criteria(session: Session, id: int) -> RawCriteriaSchema:
    aes = await raw_criteria_crud.get(session, id)
    return aes

async def get_raw_criterias(session: Session) -> RawCriteriaSearchResults:
    aes = await raw_criteria_crud.get_multi(session)
    return aes
    pass

async def create_raw_criteria(session: Session, raw_criteria: RawCriteriaCreate) -> RawCriteriaSchema:

    new_raw_criteria = await raw_criteria_crud.create(db=session, obj_in=raw_criteria)
    return new_raw_criteria

async def update_raw_criteria(session: Session, raw_criteria: RawCriteriaCreate, raw_criteria_id: int) -> RawCriteriaSchema:
    raw_criteria_in = await raw_criteria_crud.get(db=session, id=raw_criteria_id)
    if raw_criteria_in:
        upd_raw_criteria = await raw_criteria_crud.update(db=session, db_obj=raw_criteria_in, obj_in=raw_criteria)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Raw criteria id: {raw_criteria_id} not found for update.") 

