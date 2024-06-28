from .base import CRUDBase
from gearbox.models import Criterion
from gearbox.schemas import CriterionCreate, CriterionSearchResults
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc

class CRUDCriterion(CRUDBase [Criterion, CriterionCreate, CriterionSearchResults]):
    ...

criterion_crud = CRUDCriterion(Criterion)