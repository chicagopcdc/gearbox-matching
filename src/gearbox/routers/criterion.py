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
from ..schemas import Criterion
from ..crud.criterion import get_all_criteria
from .. import deps
from .. import auth 

mod = APIRouter()

# auto_error=False prevents FastAPI from raises a 403 when the request is missing
# an Authorization header. Instead, we want to return a 401 to signify that we did
# not recieve valid credentials
# bearer = HTTPBearer(auto_error=False)

@mod.get("/criteria", response_model=List[Criterion], dependencies=[ Depends(auth.authenticate)])
async def get_criteria(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    auth_header = str(request.headers.get("Authorization",""))
    criteria = await get_all_criteria(session)
    return JSONResponse(jsonable_encoder(criteria), status.HTTP_200_OK)    
    """
    THIS ENDPOINT SHOULD RETURN ALL CRITERION WITH ASSOCIATED VALUE, INPUT_TYPE, ONTOLOGY_CODE
    DISPLAY_RULES, TRIGGERED_BY, and TAG INFORMAITON
    """
@mod.post("/criterion", response_model=Criterion,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: Criterion,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    auth_header = str(request.headers.get("Authorization",""))
    value = await add_value(session, body)
    return JSONResponse(jsonable_encoder(value), status.HTTP_201_CREATED)
    """

def init_app(app):
    app.include_router(mod, tags=["criteria","criterion"])
