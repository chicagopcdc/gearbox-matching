from .base import CRUDBase
from gearbox.models import Criterion
from gearbox.schemas import CriterionCreate, CriterionSearchResults
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc

class CRUDCriterion(CRUDBase [Criterion, CriterionCreate, CriterionSearchResults]):

    async def get_criteria_by_status(self, current_session: Session, criterion_status: str):

        stmt = select(Criterion).where(
            Criterion.status == criterion_status).order_by(Criterion.id)
        result = await current_session.execute(stmt)
        criteria = result.unique().scalars().all()

        return criteria

criterion_crud = CRUDCriterion(Criterion)