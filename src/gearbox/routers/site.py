from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
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
from gearbox.schemas import SiteSearchResults, Site as SiteSchema, SiteCreate
from gearbox import deps
from gearbox.services import site  as site_service
from gearbox.admin_login import admin_required

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/site/{site_id}", response_model=SiteSchema, dependencies=[Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_site(
    request: Request,
    site_id: int,
    session: AsyncSession = Depends(deps.get_session),
    token: HTTPAuthorizationCredentials = Security(bearer)
):
    ret_site = await site_service.get_single_site(session, site_id)
    return JSONResponse(jsonable_encoder(ret_site), status.HTTP_200_OK)

@mod.get("/sites", response_model=SiteSearchResults, dependencies=[Depends(auth.authenticate)])
async def get_all_sites(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    token: HTTPAuthorizationCredentials = Security(bearer)
):
    sites = await site_service.get_sites(session)
    return JSONResponse(jsonable_encoder(sites), status.HTTP_200_OK)

@mod.post("/site", response_model=SiteSchema,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: SiteCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    new_site = await site_service.create_site(session, body)
    await session.commit()
    return JSONResponse(new_site, status.HTTP_201_CREATED)

@mod.post("/update-site/{site_id}", response_model=SiteSchema, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    site_id: int,
    body: dict,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    upd_site = await site_service.update_site(session=session, site=body, site_id=site_id)
    return JSONResponse(jsonable_encoder(upd_site), status.HTTP_201_CREATED)

def init_app(app):
    app.include_router(mod, tags=["site"])
