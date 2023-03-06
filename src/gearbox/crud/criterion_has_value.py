from .base import CRUDBase
from gearbox.models import CriterionHasValue
from gearbox.schemas import CriterionHasValueCreate, CriterionHasValueSearchResults

class CRUDCriterionHasValue(CRUDBase [CriterionHasValue, CriterionHasValueCreate, CriterionHasValueSearchResults]):
    ...
criterion_has_value_crud = CRUDCriterionHasValue(CriterionHasValue)