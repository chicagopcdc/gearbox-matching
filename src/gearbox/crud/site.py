from re import I
from sqlalchemy import func, update, select, exc
from .. import logger
from sqlalchemy.orm import Session, joinedload
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import Site, SiteHasStudy, Study, StudyLink

async def get_sites(current_session: Session):
    stmt = select(Site).options(
        joinedload(Site.studies).options(
            joinedload(SiteHasStudy.study)
        )
    )
    result = await current_session.execute(stmt)
    sites = result.unique().scalars().all()
    return sites

async def get_single_site(current_session: Session, site_id: int):
    stmt = select(Site).options(
        joinedload(Site.studies).options(
            joinedload(SiteHasStudy.study)
        )
    ).where(Site.id == site_id)
    result = await current_session.execute(stmt)
    site = result.unique().scalars().all()
    return site