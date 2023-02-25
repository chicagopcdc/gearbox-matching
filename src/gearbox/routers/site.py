from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends
from fastapi import APIRouter
from . import logger
from ..util import status
from gearbox import auth
from gearbox.schemas import SiteSearchResults, Site as SiteSchema, SiteCreate
from gearbox import deps
from gearbox.services import site  as site_service
from gearbox.admin_login import admin_required

mod = APIRouter()

@mod.get("/site/{site_id}", response_model=SiteSchema, dependencies=[Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_site(
    request: Request,
    site_id: int,
    session: AsyncSession = Depends(deps.get_session)
):
    ret_site = await site_service.get_site(session, site_id)
    return ret_site

@mod.get("/sites", response_model=SiteSearchResults, status_code = status.HTTP_200_OK, dependencies=[Depends(auth.authenticate)])
async def get_all_sites(
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    sites = await site_service.get_sites(session)
    return { "results": list(sites)}

@mod.post("/site", response_model=SiteSchema,status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: SiteCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    new_site = await site_service.create_site(session, body)
    await session.commit()
    return new_site

@mod.post("/update-site/{site_id}", response_model=SiteSchema, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
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
    return upd_site

def init_app(app):
    app.include_router(mod, tags=["site"])
