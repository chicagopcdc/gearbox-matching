import json
from datetime import datetime

from gearbox.models.study_algorithm_engine import Value
from . import logger
from sqlalchemy.orm import Session
from sqlalchemy import select, exc, update
from fastapi import HTTPException
from gearbox.models import Value
from gearbox.schemas import Value as ValueSchema
from gearbox.schemas import ValueCreate, ValueSearchResults
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

async def create_value(session: Session, study_algorithm_engine: ValueCreate) -> ValueSchema:
    pass

