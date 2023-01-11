from .base import CRUDBase
from gearbox.models.models import CriterionHasTag
from ..schemas import CriterionHasTagCreate, CriterionHasTagSearchResults

class CRUDCriterionHasTag(CRUDBase [CriterionHasTag, CriterionHasTagCreate, CriterionHasTagSearchResults]):
    ...
criterion_has_tag = CRUDCriterionHasTag(CriterionHasTag)