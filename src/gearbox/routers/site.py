from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import date
from time import gmtime, strftime
from . import logger
from ..util import status
from starlette.responses import JSONResponse
from typing import List
from gearbox import auth
from gearbox.schemas import SiteSearchResults
from gearbox.crud.site import get_single_site, get_sites
from gearbox import deps

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/site/{site_id}", response_model=SiteSearchResults, dependencies=[Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
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

@mod.get("/sites", response_model=SiteSearchResults, dependencies=[Depends(auth.authenticate)])
async def get_all_sites(
    request: Request,
    session: Session = Depends(deps.get_session),
    token: HTTPAuthorizationCredentials = Security(bearer)
):
    sites = await get_sites(session)
    return JSONResponse(jsonable_encoder(sites), status.HTTP_200_OK)

def init_app(app):
    app.include_router(mod, tags=["site"])
