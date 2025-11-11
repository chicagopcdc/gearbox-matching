from .base import CRUDBase
from gearbox.models import Criterion, DisplayRules
from gearbox.schemas import CriterionCreate, Criterion as CriterionSchema
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc
from typing import List

class CRUDCriterion(CRUDBase [Criterion, CriterionCreate, CriterionSchema]):

    async def get_criterion_id_by_code(self, db: Session, code: str) -> CriterionSchema:
        stmt = select(Criterion.id).where(Criterion.code == code)
        result = await db.execute(stmt)
        criterion_id = result.unique().scalars().first()
        return criterion_id

    async def get_criteria_not_exist_in_match_form(self, db: Session) -> List[CriterionSchema]:
        subq = (select(DisplayRules.criterion_id).where(Criterion.id == DisplayRules.criterion_id)).exists()
        stmt = select(Criterion).where(Criterion.active == True).where(~subq)
        result = await db.execute(stmt)
        criteria = result.unique().scalars().all()
        return criteria

criterion_crud = CRUDCriterion(Criterion)