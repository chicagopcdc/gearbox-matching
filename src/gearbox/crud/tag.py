from sqlalchemy import update, select, exc
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import Tag
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..util import status

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_all_tags(current_session: Session):
    stmt = select(Tag)
    result = await current_session.execute(stmt)
    tags = result.scalars().all()
    return tags

async def add_tag(current_session: Session, data: dict):

    new_tag = Tag(code=data.code,
        type=data.type
        )
    current_session.add(new_tag)
    try:
        await current_session.commit()
        return new_tag
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Unique constraint ERROR: code: {data.code} type: {data.type} already exists")
    except exc.SQLAlchemyError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")