from .base import CRUDBase
from typing import List
from gearbox.models import StudyVersion, EligibilityCriteria
from gearbox.schemas import StudyVersionSearchResults, StudyVersionCreate, StudyVersion as StudyVersionSchema
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc, or_
from gearbox.util.types import StudyVersionStatus 
from fastapi import HTTPException
from gearbox.util import status

class CRUDStudyVersion(CRUDBase [StudyVersion, StudyVersionSchema, StudyVersionCreate]):

    async def get_study_versions_for_adjudication(self, current_session: Session):

        stmt = select(StudyVersion).where(
                (or_(StudyVersion.status == StudyVersionStatus.IN_PROCESS,
                        StudyVersion.status == StudyVersionStatus.NEW))
        ).order_by(StudyVersion.id)

        result = await current_session.execute(stmt)
        study_versions = result.unique().scalars().all()
        return study_versions
    
    async def get_study_version_ec_id(self, current_session: Session, eligibility_criteria_id: int):

        stmt = select(StudyVersion).where(StudyVersion.eligibility_criteria_id == eligibility_criteria_id)

        result = await current_session.execute(stmt)
        study_version = result.unique().scalars().first()
        return study_version

    async def get_latest_study_version(self, current_session: Session, study_id: int) -> StudyVersionSchema:

        study_version = None
        try:
            max_ver_subq = select(func.max(StudyVersion.study_version_num)) \
                .where(StudyVersion.study_id == study_id)
            stmt = select(StudyVersion).where(StudyVersion.study_id == study_id). \
                where(StudyVersion.study_version_num == max_ver_subq)
                #join(max_ver_subq, StudyVersion.study_version_num == max_ver_subq)
            result = await current_session.execute(stmt)
            study_version = result.unique().scalars().first()
        except exc.SQLAlchemyError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")    

        return study_version

    
study_version_crud = CRUDStudyVersion(StudyVersion)
