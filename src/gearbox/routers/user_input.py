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
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
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

from .. import config
from ..models.models import SavedInput
from ..schemas import SavedInputSearchResults, UploadSavedInput
from ..crud.saved_input import add_saved_input, get_latest_saved_input, update_saved_input
from .. import deps
from .. import auth 

### FOR TESTING ADMIN AUTHZ REMOVE AFTER TEST###
from ..admin_login import admin_required
### END FOR TESTING ADMIN AUTHZ ###

from cdislogging import get_logger
logger = get_logger(__name__)

mod = APIRouter()

# auto_error=False prevents FastAPI from raises a 403 when the request is missing
# an Authorization header. Instead, we want to return a 401 to signify that we did
# not recieve valid credentials
# bearer = HTTPBearer(auto_error=False)

@mod.post("/user-input", response_model=SavedInputSearchResults)
### FOR TESTING ADMIN AUTHZ REMOVE AFTER TEST###
##@mod.post("/user-input", response_model=SavedInputSearchResults, dependencies=[Depends(admin_required) ])
### END FOR TESTING ADMIN AUTHZ ###
async def save_object(
    body: UploadSavedInput,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    """
        Save user form input, return saved object list to the user.

        Args:
            body (UploadSavedInput): input body for saving input
            request (Request): starlette request (which contains reference to FastAPI app)
            token (HTTPAuthorizationCredentials, optional): bearer token
    """
    data = body.data
    data = data or []
    saved_input_id = body.id

    auth_header = str(request.headers.get("Authorization",""))

    if not saved_input_id:
        #TODO add try catch around the int()
        results = await add_saved_input(session, int(user_id), data)
    else:
        results = await update_saved_input(session, int(user_id), saved_input_id, data)

    response = {
        "results": results.data,
        "id": results.id
    }

    return JSONResponse(response, HTTP_201_CREATED)

@mod.get("/user-input/latest", response_model=SavedInputSearchResults)
async def get_object_latest(
    request: Request,
    session: Session = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
) -> JSONResponse:
    """
    Attempt to fetch the latest version of the user saved search, 
    return the saved object.

    Args:
        request (Request): starlette request (which contains reference to FastAPI app)
        token (HTTPAuthorizationCredentials, optional): bearer token

    Returns:
        200: { "results": [{id: 1, "value": ""}] }
        404: if the obj is not found
    """
    auth_header = str(request.headers.get("Authorization",""))
    saved_user_input = await get_latest_saved_input(session, int(user_id))

    if not saved_user_input:
        raise HTTPException(HTTP_404_NOT_FOUND, f"Saved input not found for user '{user_id}'")

    response = {
        "results": saved_user_input.data,
        "id": saved_user_input.id
    }

    return JSONResponse(response, HTTP_200_OK) 

def init_app(app):
    app.include_router(mod, tags=["user_input"])
