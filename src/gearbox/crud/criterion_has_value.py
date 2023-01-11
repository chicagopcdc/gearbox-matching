from .base import CRUDBase
from gearbox.models.models import CriterionHasValue
from ..schemas import CriterionHasValueCreate, CriterionHasValueSearchResults

class CRUDCriterionHasValue(CRUDBase [CriterionHasValue, CriterionHasValueCreate, CriterionHasValueSearchResults]):
    ...
criterion_has_value = CRUDCriterionHasValue(CriterionHasValue)