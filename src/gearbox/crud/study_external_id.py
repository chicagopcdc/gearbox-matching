from .base import CRUDBase
from gearbox.models import StudyExternalId
from gearbox.schemas import StudyExternalIdCreate, StudyExternalIdSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import select

class CRUDStudyExternalId(CRUDBase [StudyExternalId, StudyExternalIdCreate, StudyExternalIdSearchResults]):
    
    async def get_study_id_by_ext_id(self, db: Session, ext_id: str) -> int: 
        stmt = select(StudyExternalId.study_id).where(StudyExternalId.ext_id == ext_id)
        result = await db.execute(stmt)
        study_id = result.unique().scalars().first()
        return study_id

study_external_id_crud = CRUDStudyExternalId(StudyExternalId)