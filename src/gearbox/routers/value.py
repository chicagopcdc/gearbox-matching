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
from ..util import status
from starlette.responses import JSONResponse
from ..admin_login import admin_required

from .. import config
from ..schemas import ValueCreate, ValueSearchResult
from ..crud.value import add_value, get_all_values
from .. import deps
from .. import auth 

mod = APIRouter()

# auto_error=False prevents FastAPI from raises a 403 when the request is missing
# an Authorization header. Instead, we want to return a 401 to signify that we did
# not recieve valid credentials
# bearer = HTTPBearer(auto_error=False)


@mod.get("/values", response_model=List[ValueSearchResult], dependencies=[ Depends(auth.authenticate)])
async def get_values(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    auth_header = str(request.headers.get("Authorization",""))
    values = await get_all_values(session)
    return JSONResponse(jsonable_encoder(values), status.HTTP_200_OK)

@mod.post("/value", response_model=ValueSearchResult,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: ValueCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    auth_header = str(request.headers.get("Authorization",""))
    value = await add_value(session, body)
    return JSONResponse(jsonable_encoder(value), status.HTTP_201_CREATED)

#TO DO: endpoint that returns all values to the front-end

def init_app(app):
    app.include_router(mod, tags=["value","values"])
