from collections.abc import Iterable
from enum import Enum
from . import config, logger
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



@mod.post("/save")
async def save_object(
    body: UploadSavedInput,
    request: Request,
    db: Session = Depends(deps.get_db),
    token: HTTPAuthorizationCredentials = Security(bearer),
    response_model=SavedInputSearchResults
):
    """
    Save user form input, return saved object list to the user.

    Args:
        body (UploadSavedInput): input body for saving input
        request (Request): starlette request (which contains reference to FastAPI app)
        token (HTTPAuthorizationCredentials, optional): bearer token
    """
    try:
        issuer = None
        allowed_issuers = None

        # override token iss 
        if config.FORCE_ISSUER:
          issuer = config.USER_API
          allowed_issuers =  list(config.ALLOWED_ISSUERS)
          

        # NOTE: token can be None if no Authorization header was provided, we expect
        #       this to cause a downstream exception since it is invalid
        token_claims = await access_token("user", "openid", issuer=issuer, allowed_issuers=allowed_issuers, purpose="access")(token)
    except Exception as exc:
        logger.error(exc, exc_info=True)
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            f"Could not verify, parse, and/or validate scope from provided access token.",
        )

    data = body.data
    data = data or []
    saved_input_id = body.id

    # get user id from token claims
    user_id = token_claims.get("sub")
    auth_header = str(request.headers.get("Authorization", ""))

    if not saved_input_id:
        #TODO add try catch around the int()
        # data = await add_saved_input(db, int(user_id), data)
        results = add_saved_input(db, int(user_id), data)
    else:
        results = update_saved_input(db, int(user_id), saved_input_id, data)

    response = {
        "results": results.data,
        "id": results.id
    }

    return JSONResponse(response, HTTP_201_CREATED)


@mod.get("/save/latest", response_model=SavedInputSearchResults)
async def get_object_latest(
    request: Request,
    db: Session = Depends(deps.get_db),
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

    try:
        issuer = None
        allowed_issuers = None

        # override token iss 
        if config.FORCE_ISSUER:
          issuer = config.USER_API
          allowed_issuers =  list(config.ALLOWED_ISSUERS)
          

        # NOTE: token can be None if no Authorization header was provided, we expect
        #       this to cause a downstream exception since it is invalid
        token_claims = await access_token("user", "openid", issuer=issuer, allowed_issuers=allowed_issuers, purpose="access")(token)
    except Exception as exc:
        logger.error(exc, exc_info=True)
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            f"Could not verify, parse, and/or validate scope from provided access token.",
        )

    user_id = token_claims.get("sub")

    #TODO add try catch around the int()
    # saved_user_input = await get_latest_saved_input(db, int(user_id))
    saved_user_input = get_latest_saved_input(db, int(user_id))

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
    app.include_router(mod, tags=["Save"])