from .base import CRUDBase
from gearbox.models import SiteHasStudy
from gearbox.schemas import SiteHasStudyCreate, SiteHasStudySearchResults
from sqlalchemy.orm import Session 
from sqlalchemy import update, exc
from typing import List
from fastapi import HTTPException
from gearbox.util import status
from cdislogging import get_logger
logger = get_logger(__name__)

class CRUDSiteHasStudy(CRUDBase [SiteHasStudy, SiteHasStudyCreate, SiteHasStudySearchResults]):

    async def set_active_all_rows(self, db: Session, ids: List[int], active_upd: bool) -> bool: 
        try:
            stmt = ( update(SiteHasStudy)
                .values(active=active_upd)
                .where(SiteHasStudy.study_id.in_(ids))
            )
            res = await db.execute(stmt)
            db.commit()
        except exc.SQLAlchemyError as e:
            db.rollback()
            logger.error(f"SQL ERROR IN CRUDSiteHasStudy.set_active_all_rows method: {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        
        return True

site_has_study_crud = CRUDSiteHasStudy(SiteHasStudy)