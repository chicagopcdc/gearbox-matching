import datetime
from re import I
from sqlalchemy import func, update, select, exc
from .. import logger
from sqlalchemy.orm import Session, joinedload
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import Site, SiteHasStudy
from gearbox.schemas import SavedInputDB
from fastapi import HTTPException
from asyncpg import UniqueViolationError
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

async def get_sites(current_session: Session):
    stmt = select(Site).options(
        joinedload(Site.studies).options(
            joinedload(SiteHasStudy.study)
        )
    )
    logger.info(f"HERE IN get_sites!!!!!!!!!!!!!!!!!!!")
    result = await current_session.execute(stmt)
    sites = result.unique().scalars().all()
    return sites

async def get_single_site(current_session: Session, site_id: int):
    logger.info("HERE IN get_single_site......")
    stmt = select(Site).options(
        joinedload(Site.studies).options(
            joinedload(SiteHasStudy.study)
        )
    ).where(Site.id == site_id)
    result = await current_session.execute(stmt)
    sites = result.unique().scalars().all()
    return sites