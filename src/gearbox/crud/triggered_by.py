from .base import CRUDBase
from gearbox.models.models import TriggeredBy
from ..schemas import TriggeredByCreate, TriggeredBySearchResults

class CRUDTriggeredBy(CRUDBase [TriggeredBy, TriggeredByCreate, TriggeredBySearchResults]):
    ...
triggered_by_crud = CRUDTriggeredBy(TriggeredBy)