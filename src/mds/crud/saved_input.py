import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from mds.models.models import SavedInput
from mds.schemas import SavedInputDB
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



# async def get_all_saved_input(current_session: Session, logged_user_id: int):
def get_all_saved_input(current_session: Session, logged_user_id: int):
    # saved_inputs = await current_session.query(SavedInput).filter_by(user_id=logged_user_id).all()
    saved_inputs = current_session.query(SavedInput).filter_by(user_id=logged_user_id).all()
    return saved_inputs


# async def get_latest_saved_input(current_session: Session, user_id: int):
def get_latest_saved_input(current_session: Session, user_id: int):
    # saved_input = await current_session.query(SavedInput).filter_by(user_id=user_id).order_by(SavedInput.create_date.desc()).first()
    saved_input = current_session.query(SavedInput).filter_by(user_id=user_id).order_by(SavedInput.create_date.desc()).first()
    
    return saved_input


# async def add_saved_input(current_session: Session, user_id: int, data: dict):   #data: Any
def add_saved_input(current_session: Session, user_id: int, data: dict):
    new_input = SavedInput(user_id=user_id, 
                            create_date=datetime.datetime.utcnow(),
                            update_date=datetime.datetime.utcnow(),
                            data=data)

    current_session.add(new_input)
    # await current_session.commit()
    current_session.commit()

    return new_input

def update_saved_input(current_session: Session, user_id: int, saved_input_id: int, data: dict):
    # number_updated_rows = current_session.query(SavedInput).filter(SavedInput.id == saved_input_id, SavedInput.user_id == user_id).update({SavedInput.data: data})
    saved_input = current_session.query(SavedInput).filter(SavedInput.id == saved_input_id, SavedInput.user_id == user_id).first()
    saved_input.data = data
    current_session.commit()
    return saved_input



# async def _add_saved_input(user_id: int, data: dict):
#     try:
#         rv = (
#             await SavedInput.insert()
#             .values(user_id=user_id, data=data, create_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow())
#             .returning(*SavedInput)
#             .gino.first()
#         )
#     except UniqueViolationError:
#         raise HTTPException(HTTP_409_CONFLICT, f"Metadata GUID conflict: {user_id}")

#     return rv["data"]


# async def _get_latest_saved_input(user_id: int):
#     try:
#         rv = (
#             # await SavedInput.query.where(SavedInput.user_id=user_id).order_by(SavedInput.create_date.desc()).gino.first()
#             await SavedInput.query.where(SavedInput.user_id == user_id).gino.first()
#         )
#     except UniqueViolationError:
#         raise HTTPException(HTTP_409_CONFLICT, f"Metadata GUID conflict: {user_id}")

#     print(rv)
#     print(rv.json())
#     # print(rv["data"])

#     return rv #["data"]


