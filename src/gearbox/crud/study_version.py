from .base import CRUDBase
from typing import List
from gearbox.models import StudyVersion, EligibilityCriteria
from gearbox.schemas import StudyVersionSearchResults, StudyVersionCreate, StudyVersion as StudyVersionSchema
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc, or_
from gearbox.util.types import StudyVersionStatus 

class CRUDStudyVersion(CRUDBase [StudyVersion, StudyVersionCreate, StudyVersionSearchResults]):

    """ REPLACE WITH GET MULTI PASS WHERE CLAUSE AS PARAM
    async def get_study_versions_by_status(self, current_session: Session, study_version_status: str) -> List[StudyVersionSchema]:

        stmt = select(StudyVersion).where(
            StudyVersion.status == study_version_status).order_by(StudyVersion.id)
        result = await current_session.execute(stmt)
        studies = result.unique().scalars().all()

        return studies

    async def get_study_versions_by_status(self, current_session: Session, study_version_status: str, study_id: int) -> List[StudyVersionSchema]:

        stmt = select(StudyVersion).where(
            StudyVersion.status == study_version_status).where(
                StudyVersion.study_id == study_id
                ).order_by(StudyVersion.id)
        result = await current_session.execute(stmt)
        studies = result.unique().scalars().all()

        return studies
    """
    async def get_study_versions_for_adjudication(self, current_session: Session):

        stmt = select(StudyVersion).where(
                (or_(StudyVersion.status == StudyVersionStatus.IN_PROCESS,
                        StudyVersion.status == StudyVersionStatus.NEW))
        ).order_by(StudyVersion.id)

        result = await current_session.execute(stmt)
        studies = result.unique().scalars().all()
        return studies
    
study_version_crud = CRUDStudyVersion(StudyVersion)
