import json
from datetime import datetime

from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import exc 
from fastapi import HTTPException
from gearbox.schemas import SiteCreate, SiteSearchResults, Site as SiteSchema
from gearbox.util import status
from gearbox.crud import site_crud

async def get_site_info(session: Session, id: int) -> SiteSchema:
    aes = await site_crud.get_site_info(session, id)
    return aes

async def get_site_info(session: Session) -> SiteSearchResults:
    aes = await site_crud.get_sites_info(session)
    return aes
    pass

async def get_site(session: Session, id: int) -> SiteSchema:
    aes = await site_crud.get(session, id)
    return aes

async def get_sites(session: Session) -> SiteSearchResults:
    aes = await site_crud.get_multi(session)
    return aes

async def create_site(session: Session, site: SiteCreate) -> SiteSchema:
    new_site = await site_crud.create(db=session, obj_in=site)
    return new_site

async def update_site(session: Session, site: SiteCreate, site_id: int) -> SiteSchema:
    site_in = await site_crud.get(db=session, id=site_id)
    if site_in:
        upd_site = await site_crud.update(db=session, db_obj=site_in, obj_in=site)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Site for id: {site_id} not found for update.") 
    await session.commit() 
    return upd_site