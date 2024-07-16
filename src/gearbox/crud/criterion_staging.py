from .base import CRUDBase
from gearbox.models import CriterionStaging as CriterionStagingModel
from gearbox.schemas import CriterionStaging, CriterionStagingCreate, CriterionStagingSearchResults
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc

class CRUDCriterionStaging(CRUDBase [CriterionStaging, CriterionStagingCreate, CriterionStagingSearchResults]):
    ...

criterion_staging_crud = CRUDCriterionStaging(CriterionStagingModel)