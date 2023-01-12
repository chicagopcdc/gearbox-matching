from .base import CRUDBase
from gearbox.models import Criterion
from gearbox.schemas import CriterionCreate, CriterionSearchResults

class CRUDCriterion(CRUDBase [Criterion, CriterionCreate, CriterionSearchResults]):
    ...
criterion_crud = CRUDCriterion(Criterion)