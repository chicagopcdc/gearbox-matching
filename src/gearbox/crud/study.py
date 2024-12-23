from re import I
from .base import CRUDBase
from sqlalchemy import update, select, exc, subquery
from sqlalchemy.orm import Session, joinedload
from typing import  List 
from gearbox.models import Study, SiteHasStudy, Source, StudyVersion
from gearbox.schemas import StudySearchResults, StudyCreate
from fastapi import HTTPException
from gearbox.util import status
from gearbox.util.types import StudyVersionStatus
from cdislogging import get_logger
logger = get_logger(__name__)

class CRUDStudy(CRUDBase [Study, StudyCreate, StudySearchResults]):

    # Returns study information for ACTIVE studies
    async def get_studies_info(self, current_session: Session):
        sv_subq = select(StudyVersion).where(StudyVersion.status==StudyVersionStatus.ACTIVE).subquery()
        stmt = select(Study).options(
            joinedload(Study.sites).options(
                joinedload(SiteHasStudy.site)
            ), joinedload(Study.links)
        ).where(Study.active == True).join(sv_subq, Study.id == sv_subq.c.study_id).order_by(Study.id)

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

    async def get_studies_for_update(self, db: Session, priority: int) -> List[Study]: 
        stmt = select(Study).join(Source).where(Source.priority <= priority)
        result = await db.execute(stmt)
        studies= result.unique().scalars().all()
        return studies

    async def get_existing_studies(self, db: Session) -> List[str]: 
        stmt = select(Study.code)
        result = await db.execute(stmt)
        study_codes = result.unique().scalars().all()
        return study_codes

    async def set_active_all_rows(self, db: Session, ids: List[int], active_upd: bool) -> bool: 
        try:
            stmt = ( update(Study)
                .values(active=active_upd)
                .where(Study.id.in_(ids))
            )
            res = await db.execute(stmt)
            db.commit()
        except exc.SQLAlchemyError as e:
            db.rollback()
            logger.error(f"SQL ERROR IN CRUDStudy.set_active_all_rows method: {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        
        return True

study_crud = CRUDStudy(Study)