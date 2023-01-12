from .base import CRUDBase
from gearbox.models import CriterionHasTag
from gearbox.schemas import CriterionHasTagCreate, CriterionHasTagSearchResults

class CRUDCriterionHasTag(CRUDBase [CriterionHasTag, CriterionHasTagCreate, CriterionHasTagSearchResults]):
    ...
criterion_has_tag_crud = CRUDCriterionHasTag(CriterionHasTag)