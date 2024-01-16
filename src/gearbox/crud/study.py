from re import I
from .base import CRUDBase
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session, joinedload
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models import Study, SiteHasStudy, Source
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
    
    async def get_study_ids_for_source(self, db: Session, source: str) -> List[int]: 
        stmt = select(Study.id).join(Source).where(Source.source == source)
        result = await db.execute(stmt)
        study_ids = result.unique().scalars().all()
        return study_ids

    async def get_studies_for_update(self, db: Session, priority: int) -> List[str]: 
        stmt = select(Study.code).join(Source).where(Source.priority <= priority)
        result = await db.execute(stmt)
        study_codes = result.unique().scalars().all()
        return study_codes

    async def get_existing_studies(self, db: Session) -> List[str]: 
        stmt = select(Study.code)
        result = await db.execute(stmt)
        study_codes = result.unique().scalars().all()
        return study_codes


    async def set_active_all_rows(self, db: Session, ids: List[int], active_upd: bool) -> bool: 
        stmt = ( update(Study)
            .values(active=active_upd)
            .where(Study.id in ids)
        )
        res = await db.execute(stmt)
        db.commit()
        return True

study_crud = CRUDStudy(Study)