from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import date
from time import gmtime, strftime
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
from typing import List
from .. import auth
from ..schemas import SiteSchema, SiteResponse
from ..crud.site import get_single_site, get_sites
from .. import deps

import logging
logger = logging.getLogger('gb-logger')

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/site/{site_id}", response_model=SiteResponse, dependencies=[Depends(auth.authenticate)], status_code=HTTP_200_OK)
async def get_site(
    request: Request,
    site_id: int,
    session: Session = Depends(deps.get_session),
    token: HTTPAuthorizationCredentials = Security(bearer)
):
    results = await get_single_site(session, site_id)

    response = {
                "current_date": date.today().strftime("%B %d, %Y"),
                "current_time": strftime("%H:%M:%S +0000", gmtime()),
                "status": "OK",
                "body": results
    }

    return response

@mod.get("/sites", response_model=SiteResponse, dependencies=[Depends(auth.authenticate)], status_code=HTTP_200_OK)
async def get_all_sites(
    request: Request,
    session: Session = Depends(deps.get_session),
    token: HTTPAuthorizationCredentials = Security(bearer)
):
    results = await get_sites(session)

    response = {
                "current_date": date.today().strftime("%B %d, %Y"),
                "current_time": strftime("%H:%M:%S +0000", gmtime()),
                "status": "OK",
                "body": results
    }

    return response

def init_app(app):
    app.include_router(mod, tags=["site"])
