from .base import CRUDBase
from gearbox.models import StudyLink
from gearbox.schemas import StudyLinkSearchResults, StudyLinkCreate
from sqlalchemy.orm import Session 
from sqlalchemy import update
from typing import List

class CRUDStudyLink(CRUDBase [StudyLink, StudyLinkCreate, StudyLinkSearchResults]):

    async def set_active_all_rows(self, db: Session, ids: List[int], active_upd: bool) -> bool: 
        stmt = ( update(StudyLink)
            .values(active=active_upd)
            .where(StudyLink.study_id in ids)
        )
        res = await db.execute(stmt)
        db.commit()

        return True
study_link_crud = CRUDStudyLink(StudyLink)