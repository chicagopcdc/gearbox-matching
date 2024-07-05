from .base import CRUDBase
from gearbox.models import RawCriteria, EligibilityCriteria
from gearbox.schemas import RawCriteriaCreate, RawCriteriaSearchResults
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc

class CRUDRawCriteria(CRUDBase [RawCriteria, RawCriteriaCreate, RawCriteriaSearchResults]):

    async def get_raw_criteria_by_status(self, current_session: Session, eligibility_criteria_status: str):

        stmt = select(RawCriteria).where(
            RawCriteria.eligibility_criteria(EligibilityCriteria.status == 
                eligibility_criteria_status)
        ).order_by(RawCriteria.id)
        result = await current_session.execute(stmt)
        studies = result.unique().scalars().all()

        return studies

raw_criteria_crud = CRUDRawCriteria(RawCriteria)