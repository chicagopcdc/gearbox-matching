import datetime
from re import I
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import SavedInput
from fastapi import HTTPException
from asyncpg import UniqueViolationError
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

import logging
logger = logging.getLogger('gb-logger')



async def get_all_saved_input(current_session: Session, logged_user_id: int):
    stmt = select(SavedInput).where(SavedInput.user_id==logged_user_id)
    result = await current_session.execute(stmt)
    saved_inputs = result.scalars().all()
    return saved_inputs


async def get_latest_saved_input(current_session: Session, user_id: int):
    stmt = select(SavedInput).where(SavedInput.user_id==user_id).order_by(SavedInput.create_date.desc())
    try:
        result = await current_session.execute(stmt)
        # RETURNS OBJECT OF TYPE SavedInput
        saved_input = result.scalars().first()
        return saved_input
    except exc.SQLAlchemyError as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}")
    


async def add_saved_input(current_session: Session, user_id: int, data: dict):
    new_input = SavedInput(user_id=user_id, 
                            create_date=datetime.datetime.utcnow(),
                            update_date=datetime.datetime.utcnow(),
                            data=data)
    current_session.add(new_input)
    try:
        await current_session.commit()
        return new_input
    except UniqueViolationError:
        raise HTTPException(HTTP_409_CONFLICT, f"Metadata GUID conflict: {user_id}")
    except exc.SQLAlchemyError as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}")

async def update_saved_input(current_session: Session, user_id: int, saved_input_id: int, data: dict):
    # SELECT AND LOCK ROW FOR UPDATE
    stmt = select(SavedInput).where(SavedInput.id == saved_input_id, SavedInput.user_id == user_id).with_for_update(nowait=True)
    stmt.execution_options(synchronize_session="fetch")

    try:
        result = await current_session.execute(stmt)
        saved_input = result.scalars().first()
        saved_input.data = data
    except exc.SQLAlchemyError as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}")

    try:
        await current_session.commit()
        return saved_input 
    except UniqueViolationError:
        raise HTTPException(HTTP_409_CONFLICT, f"User id conflict: {user_id}")
    except exc.SQLAlchemyError as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}")
