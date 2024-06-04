from .base import CRUDBase
from gearbox.models import StudyVersion, EligibilityCriteriaInfo, Study
from gearbox.schemas import StudyVersionSearchResults, StudyVersionCreate
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc
from gearbox.util.types import EligibilityCriteriaInfoStatus

class CRUDStudyVersion(CRUDBase [StudyVersion, StudyVersionCreate, StudyVersionSearchResults]):

    async def get_study_versions_by_status(self, current_session: Session, eligibility_criteria_info_status: str):

        stmt = select(StudyVersion).where(
            StudyVersion.eligibility_criteria_infos.any(EligibilityCriteriaInfo.status == 
                eligibility_criteria_info_status)
        ).order_by(StudyVersion.id)
        result = await current_session.execute(stmt)
        studies = result.unique().scalars().all()

        return studies

study_version_crud = CRUDStudyVersion(StudyVersion)
