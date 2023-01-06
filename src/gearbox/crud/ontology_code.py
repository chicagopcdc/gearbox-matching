from sqlalchemy import update, select, exc
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import OntologyCode
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..util import status

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_all_ontology_codes(current_session: Session):
    stmt = select(OntologyCode)
    result = await current_session.execute(stmt)
    ontology_codes = result.scalars().all()
    return ontology_codes

async def add_ontology_code(current_session: Session, data: dict):

    new_ontology_code = OntologyCode(ontology_url=data.ontology_url,
        name=data.name,
        code=data.code,
        value=data.value,
        version=data.version
        )
    current_session.add(new_ontology_code)
    try:
        await current_session.commit()
        return new_ontology_code
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Unique constraint ERROR: ontology_url: {data.ontology_url} name: {data.name} code: {data.code} value: {data.value} version: {data.version} already exists.")
    except exc.SQLAlchemyError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")