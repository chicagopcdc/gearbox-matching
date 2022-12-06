from re import I
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session, joinedload
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models.models import Study, SiteHasStudy

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_studies(current_session: Session):
    stmt = select(Study).options(
        joinedload(Study.sites).options(
            joinedload(SiteHasStudy.site)
        ), joinedload(Study.links)
    ).where(Study.active == True).order_by(Study.id)
    result = await current_session.execute(stmt)
    studies = result.unique().scalars().all()
    return studies

async def get_single_study(current_session: Session, study_id: int):
    stmt = select(Study).options(
        joinedload(Study.sites).options(
            joinedload(SiteHasStudy.site)
        ), joinedload(Study.links)
    ).where(Study.id == study_id)
    result = await current_session.execute(stmt)
    sites = result.unique().scalars().all()
    return sites
