from .base import CRUDBase
from gearbox.models import SiteHasStudy
from gearbox.schemas import SiteHasStudyCreate, SiteHasStudySearchResults
from sqlalchemy.orm import Session 
from sqlalchemy import update
from typing import List

class CRUDSiteHasStudy(CRUDBase [SiteHasStudy, SiteHasStudyCreate, SiteHasStudySearchResults]):

    async def set_active_all_rows(self, db: Session, ids: List[int], active_upd: bool) -> bool: 
        stmt = ( update(SiteHasStudy)
            .values(active=active_upd)
            .where(SiteHasStudy.study_id in ids)
        )
        res = await db.execute(stmt)
        db.commit()

        return True

site_has_study_crud = CRUDSiteHasStudy(SiteHasStudy)