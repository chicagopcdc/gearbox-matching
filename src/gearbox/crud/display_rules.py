from .base import CRUDBase
from gearbox.models import DisplayRules
from gearbox.schemas import DisplayRulesCreate, DisplayRules as DisplayRulesSchema 

class CRUDDisplayRules(CRUDBase [DisplayRules, DisplayRulesCreate, DisplayRulesSchema]):
    ...
display_rules_crud = CRUDDisplayRules(DisplayRules)

