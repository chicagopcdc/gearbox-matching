from .base import CRUDBase
from gearbox.models import StudyLink
from gearbox.schemas import StudyLinkSearchResults, StudyLinkCreate
from sqlalchemy.orm import Session 
from sqlalchemy import update, exc
from typing import List
from fastapi import HTTPException
from gearbox.util import status
from cdislogging import get_logger
logger = get_logger(__name__)

class CRUDStudyLink(CRUDBase [StudyLink, StudyLinkCreate, StudyLinkSearchResults]):

    async def set_active_all_rows(self, db: Session, ids: List[int], active_upd: bool) -> bool: 
        try:
            stmt = ( update(StudyLink)
                .values(active=active_upd)
                .where(StudyLink.study_id.in_(ids))
            )
            await db.execute(stmt)
            await db.commit()
        except exc.SQLAlchemyError as e:
            db.rollback()
            logger.error(f"SQL ERROR IN CRUDStudyLink.set_active_all_rows method: {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        
        return True

study_link_crud = CRUDStudyLink(StudyLink)