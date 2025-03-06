from .base import CRUDBase
from gearbox.models import CriterionStaging as CriterionStagingModel, Criterion as CriterionModel
from gearbox.schemas import CriterionStaging as CriterionStagingSchema, CriterionStagingCreate 
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc
from gearbox.util.types import AdjudicationStatus, EchcAdjudicationStatus
from typing import List

class CRUDCriterionStaging(CRUDBase [CriterionStagingModel, CriterionStagingSchema, CriterionStagingCreate ]):
    async def get_criterion_staging_by_ec_id(self, db: Session, eligibility_criteria_id: int):
        stmt = select(CriterionStagingModel).where(CriterionStagingModel.eligibility_criteria_id == eligibility_criteria_id)
        result = await db.execute(stmt)
        cs = result.unique().scalars().all()
        return cs 

    async def get_criterion_staging_missing_criterion_id(self, db: Session, eligibility_criteria_id: int):
        stmt = select(CriterionStagingModel).where(CriterionStagingModel.eligibility_criteria_id == eligibility_criteria_id).where(CriterionStagingModel.criterion_id == None)
        result = await db.execute(stmt)
        cs = result.unique().scalars().all()
        return cs 

    async def get_criterion_staging_by_criterion_adjudication_status(self, db: Session, eligibility_criteria_id: int, adjudication_status: List[AdjudicationStatus]):
        stmt = select(CriterionStagingModel).where(CriterionStagingModel.eligibility_criteria_id == eligibility_criteria_id).where(CriterionStagingModel.criterion_adjudication_status.in_(adjudication_status))
        result = await db.execute(stmt)
        cs = result.unique().scalars().all()
        return cs 

    async def get_criterion_staging_by_echc_adjudication_status(self, db: Session, eligibility_criteria_id: int, echc_adjudication_status: List[EchcAdjudicationStatus]):
        stmt = select(CriterionStagingModel).where(CriterionStagingModel.eligibility_criteria_id == eligibility_criteria_id).where(CriterionStagingModel.echc_adjudication_status.in_(echc_adjudication_status))
        result = await db.execute(stmt)
        cs = result.unique().scalars().all()
        return cs 
    
    # Get all criterion_staging rows where criterion 'active' is false
    async def get_criterion_staging_inactive_criterion(self, db:Session, eligibility_criteria_id: int):
        stmt = select(CriterionStagingModel).join(CriterionModel).where(CriterionModel.active == False)
        result = await db.execute(stmt)
        cs = result.unique().scalars().all()
        return cs
    
    async def get_staged_criteria_by_ec_id(self, db:Session, eligibility_criteria_id: int):
        stmt = select(CriterionModel).join(CriterionStagingModel).where(CriterionStagingModel.eligibility_criteria_id == eligibility_criteria_id)
        result = await db.execute(stmt)
        cs = result.unique().scalars().all()
        return cs

criterion_staging_crud = CRUDCriterionStaging(CriterionStagingModel)