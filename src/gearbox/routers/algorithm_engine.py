import os
import json # REMOVE THIS AFTER DEV
import datetime
import httpx
import fastapi
from fastapi import Depends
import jwt

from collections.abc import Iterable
from enum import Enum
from typing import List
from asyncpg import UniqueViolationError
from sqlalchemy.ext.asyncio.session import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from authutils.token.fastapi import access_token
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from urllib.parse import urljoin
from pydantic import BaseModel
from fastapi import Request, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from . import logger
from gearbox.util import status
from starlette.responses import JSONResponse
from gearbox.admin_login import admin_required
from gearbox.models import AlgorithmEngine

from gearbox import config
from gearbox.schemas import AlgorithmEngineCreate, AlgorithmEngineSearchResults
from gearbox.crud import algorithm_engine_crud
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

@mod.get("/algorithm-engines", response_model=AlgorithmEngineSearchResults, dependencies=[ Depends(auth.authenticate)])
async def get_aes(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    aes = await algorithm_engine_crud.get(session)
    return JSONResponse(jsonable_encoder(aes), status.HTTP_200_OK)

# think about params here - 
@mod.get("/algorithm-engine/{algorithm_engine_id}", response_model=AlgorithmEngineSearchResults, dependencies=[ Depends(auth.authenticate)])
async def get_ae(
    algorithm_engine_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    where_list = [ f"{AlgorithmEngine.__tablename__}.id = {algorithm_engine_id}" ]
    with_only_cols_list = ["id"]
    ret_value = await algorithm_engine_crud.get(db=session, where=where_list, with_only_cols=with_only_cols_list)
    return JSONResponse(jsonable_encoder(ret_value), status.HTTP_200_OK)

@mod.post("/algorithm-engine", response_model=AlgorithmEngineSearchResults,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_ae(
    body: AlgorithmEngineCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    new_ae = await algorithm_engine_crud.create(db=session, obj_in=body)
    return JSONResponse(jsonable_encoder(new_ae), status.HTTP_201_CREATED)

def init_app(app):
    app.include_router(mod, tags=["algorithm-engine","algorithm-engines"])