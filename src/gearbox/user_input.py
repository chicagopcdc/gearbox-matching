from collections.abc import Iterable
from enum import Enum

import os

from sqlalchemy.ext.asyncio.session import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from . import config, logger, auth
from .models.models import SavedInput
from .schemas import SavedInputSearchResults, UploadSavedInput
import datetime
from typing import List
from gearbox.crud.saved_input import add_saved_input, get_latest_saved_input, update_saved_input
from gearbox import deps
from authutils.token.fastapi import access_token
from asyncpg import UniqueViolationError
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
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



mod = APIRouter()

# auto_error=False prevents FastAPI from raises a 403 when the request is missing
# an Authorization header. Instead, we want to return a 401 to signify that we did
# not recieve valid credentials
bearer = HTTPBearer(auto_error=False)

@mod.post("/user-input", response_model=SavedInputSearchResults)
async def save_object(
    body: UploadSavedInput,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    token: HTTPAuthorizationCredentials = Security(bearer)
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

    if not config.BYPASS_FENCE:
        token_claims = await auth.get_token_claims(token)
        user_id = token_claims.get("sub")
    else:
        user_id = 4

    auth_header = str(request.headers.get("Authorization", ""))

    if not saved_input_id:
        #TODO add try catch around the int()
        # data = await add_saved_input(db, int(user_id), data)
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
    token: HTTPAuthorizationCredentials = Security(bearer)
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

    if not config.BYPASS_FENCE:
        token_claims = await auth.get_token_claims(token)
        user_id = token_claims.get("sub")
    else:
        user_id = 4

    #TODO add try catch around the int()
    # saved_user_input = await get_latest_saved_input(db, int(user_id))
    saved_user_input = await get_latest_saved_input(session, int(user_id))

    if not saved_user_input:
        raise HTTPException(HTTP_404_NOT_FOUND, f"Saved input not found for user '{user_id}'")

    response = {
        "results": saved_user_input.data,
        "id": saved_user_input.id
    }

    return JSONResponse(response, HTTP_200_OK)

#     try:
#         endpoint = (
#             config.INDEXING_SERVICE_ENDPOINT.rstrip("/")
#             + f"/index/{blank_guid}/aliases"
#         )

#         # pass along the authorization header to indexd request
#         headers = {"Authorization": auth_header}
#         response = await request.app.async_client.post(
#             endpoint, json=aliases_data, headers=headers
#         )
#         response.raise_for_status()
#     except httpx.HTTPError as err:
#         # check if user has permission for resources specified
#         if err.response and err.response.status_code in (401, 403):
#             logger.error(
#                 f"Creating aliases in indexd for guid {blank_guid} failed, status code: {err.response.status_code}. Response text: {getattr(err.response, 'text')}"
#             )
#             raise HTTPException(
#                 HTTP_403_FORBIDDEN,
#                 "You do not have access to create the aliases you are trying to assign: "
#                 f"{aliases} to the guid {blank_guid}",
#             )
#         elif err.response and err.response.status_code == 409:
#             logger.error(
#                 f"Creating aliases in indexd for guid {blank_guid} failed, status code: {err.response.status_code}. Response text: {getattr(err.response, 'text')}"
#             )
#             raise HTTPException(
#                 HTTP_409_CONFLICT,
#                 f"Some of the aliases you are trying to assign to guid {blank_guid} ({aliases}) already exist",
#             )


def init_app(app):
    app.include_router(mod, tags=["user_input"])
