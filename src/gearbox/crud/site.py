from re import I
from .base import CRUDBase
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session, joinedload
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models import Site, SiteHasStudy, Study, StudyLink
from gearbox.schemas import SiteCreate, SiteSearchResults

from cdislogging import get_logger
logger = get_logger(__name__)

class CRUDSite(CRUDBase [Site, SiteCreate, SiteSearchResults]):
    async def get_sites_info(self, current_session: Session):
        stmt = select(Site).options(
            joinedload(Site.studies).options(
                joinedload(SiteHasStudy.study)
            )
        )
        result = await current_session.execute(stmt)
        # The unique() method must be invoked on this Result, as it contains results that include joined eager loads against collections
        # scalars (with an 's') returns model objects without it we get sqlalchemy.engine.row.Row objects
        sites = result.unique().scalars().all()
        return sites

    async def get_site_info(self, current_session: Session, site_id: int):
        stmt = select(Site).options(
            joinedload(Site.studies).options(
                joinedload(SiteHasStudy.study)
            )
        ).where(Site.id == site_id)
        result = await current_session.execute(stmt)
        site = result.unique().scalars().all()
        return site

site_crud = CRUDSite(Site)