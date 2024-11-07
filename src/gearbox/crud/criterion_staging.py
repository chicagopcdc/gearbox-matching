from .base import CRUDBase
from gearbox.models import CriterionStaging as CriterionStagingModel
from gearbox.schemas import CriterionStaging as CriterionStagingSchema, CriterionStagingCreate 
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc

class CRUDCriterionStaging(CRUDBase [CriterionStagingModel, CriterionStagingSchema, CriterionStagingCreate ]):
    async def get_criterion_staging_by_ec_id(self, db: Session, eligibility_criteria_id: int):
        stmt = select(CriterionStagingModel).where(CriterionStagingModel.eligibility_criteria_id == eligibility_criteria_id)
        result = await db.execute(stmt)
        cs = result.unique().scalars().all()
        return cs 

criterion_staging_crud = CRUDCriterionStaging(CriterionStagingModel)