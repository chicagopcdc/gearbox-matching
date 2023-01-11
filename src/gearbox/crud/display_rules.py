from .base import CRUDBase
from gearbox.models.models import DisplayRules
from ..schemas import DisplayRulesCreate, DisplayRulesSearchResults

class CRUDDisplayRules(CRUDBase [DisplayRules, DisplayRulesCreate, DisplayRulesSearchResults]):
    ...
display_rules_crud = CRUDDisplayRules(DisplayRules)

