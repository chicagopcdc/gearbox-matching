from .base import CRUDBase
from gearbox.models import Criterion
from gearbox.schemas import CriterionCreate, Criterion as CriterionSchema
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc

class CRUDCriterion(CRUDBase [Criterion, CriterionCreate, CriterionSchema]):

    async def get_criterion_id_by_code(self, db: Session, code: str) -> int:
        stmt = select(Criterion.id).where(Criterion.code == code)
        result = await db.execute(stmt)
        criterion_id = result.unique().scalars().first()
        return criterion_id

criterion_crud = CRUDCriterion(Criterion)