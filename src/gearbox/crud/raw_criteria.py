from .base import CRUDBase
from gearbox.models import RawCriteria, EligibilityCriteria
from gearbox.schemas import RawCriteriaCreate, RawCriteria as RawCriteriaSchema, RawCriteriaIn
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc

class CRUDRawCriteria(CRUDBase [RawCriteria, RawCriteriaSchema, RawCriteriaCreate]):

    async def get_by_eligibility_criteria_id(self, current_session: Session, eligibility_criteria_id: int) -> RawCriteriaIn:

        stmt = select(RawCriteria.data).where(
            RawCriteria.eligibility_criteria_id == eligibility_criteria_id)

        result = await current_session.execute(stmt)
        raw_criteria = result.unique().scalars().first()
        return raw_criteria

raw_criteria_crud = CRUDRawCriteria(RawCriteria)