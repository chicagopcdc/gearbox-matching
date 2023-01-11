from .base import CRUDBase
from gearbox.models.models import Criterion
from ..schemas import CriterionCreate, CriterionSearchResults

class CRUDCriterion(CRUDBase [Criterion, CriterionCreate, CriterionSearchResults]):
    ...
criterion = CRUDCriterion(Criterion)