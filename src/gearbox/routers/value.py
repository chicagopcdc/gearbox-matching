import os
import datetime
import httpx
import fastapi
from fastapi import Depends
import jwt

from collections.abc import Iterable
from enum import Enum
from typing import List
from asyncpg import UniqueViolationError
from sqlalchemy.ext.asyncio import AsyncSession
from authutils.token.fastapi import access_token
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from urllib.parse import urljoin
from pydantic import BaseModel
from fastapi import Request, Depends
from fastapi.encoders import jsonable_encoder
from . import logger
from gearbox.util import status
from starlette.responses import JSONResponse
from gearbox.admin_login import admin_required

from gearbox import config
from gearbox.schemas import ValueCreate, ValueSearchResults, Value
from gearbox.services import value as value_service
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

@mod.get("/values", response_model=ValueSearchResults, dependencies=[ Depends(auth.authenticate)])
async def get_values(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    values = await value_service.get_values(session)
    return JSONResponse(jsonable_encoder(values), status.HTTP_200_OK)

@mod.get("/value/{value_id}", response_model=Value, dependencies=[ Depends(auth.authenticate)])
async def get_value(
    value_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    ret_value = await value_service.get_value(db=session, id=value_id)
    return JSONResponse(jsonable_encoder(ret_value), status.HTTP_200_OK)

@mod.post("/value", response_model=Value,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: ValueCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    new_value = await value_service.create_value(session=session, value=body)
    return JSONResponse(jsonable_encoder(new_value), status.HTTP_201_CREATED)

@mod.post("/update-value/{value_id}", response_model=Value, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    value_id: int,
    body: dict,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    upd_value = await value_service.update_value(session=session, value=body, value_id=value_id)
    return JSONResponse(jsonable_encoder(upd_value), status.HTTP_201_CREATED)

def init_app(app):
    app.include_router(mod, tags=["value","values","update-value"])
