from .base import CRUDBase
from gearbox.models import TriggeredBy
from gearbox.schemas import TriggeredByCreate, TriggeredBySearchResults

class CRUDTriggeredBy(CRUDBase [TriggeredBy, TriggeredByCreate, TriggeredBySearchResults]):
    ...
triggered_by_crud = CRUDTriggeredBy(TriggeredBy)