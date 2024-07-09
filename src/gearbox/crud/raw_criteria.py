from .base import CRUDBase
from gearbox.models import RawCriteria, EligibilityCriteria
from gearbox.schemas import RawCriteriaCreate, RawCriteriaSearchResults
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc

class CRUDRawCriteria(CRUDBase [RawCriteria, RawCriteriaCreate, RawCriteriaSearchResults]):

    async def get_by_eligibility_criteria_id(self, current_session: Session, eligibility_criteria_id: int):
        
        stmt = select(RawCriteria).where(
            RawCriteria.eligibility_criteria_id == eligibility_criteria_id)

        result = await current_session.execute(stmt)
        raw_criteria = result.unique().scalars().first()
        return raw_criteria

raw_criteria_crud = CRUDRawCriteria(RawCriteria)