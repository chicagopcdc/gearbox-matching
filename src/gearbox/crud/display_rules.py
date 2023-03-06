from .base import CRUDBase
from gearbox.models import DisplayRules
from gearbox.schemas import DisplayRulesCreate, DisplayRulesSearchResults

class CRUDDisplayRules(CRUDBase [DisplayRules, DisplayRulesCreate, DisplayRulesSearchResults]):
    ...
display_rules_crud = CRUDDisplayRules(DisplayRules)

