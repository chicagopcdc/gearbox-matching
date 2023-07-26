from re import I
from .base import CRUDBase
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session, joinedload
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models import Study, SiteHasStudy
from gearbox.schemas import StudySearchResults, StudyCreate
from cdislogging import get_logger
logger = get_logger(__name__)

class CRUDStudy(CRUDBase [Study, StudyCreate, StudySearchResults]):

    async def get_studies_info(self, current_session: Session):
        stmt = select(Study).options(
            joinedload(Study.sites).options(
                joinedload(SiteHasStudy.site)
            ), joinedload(Study.links)
        ).where(Study.active == True).order_by(Study.id)
        result = await current_session.execute(stmt)
        studies = result.unique().scalars().all()
        return studies

    async def get_single_study_info(self, current_session: Session, study_id: int):
        stmt = select(Study).options(
            joinedload(Study.sites).options(
                joinedload(SiteHasStudy.site)
            ), joinedload(Study.links)
        ).where(Study.id == study_id)
        result = await current_session.execute(stmt)
        study = result.unique().scalars().all()
        return study

study_crud = CRUDStudy(Study)