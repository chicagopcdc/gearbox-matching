from .base import CRUDBase
from gearbox.models.models import Value
from ..schemas import ValueSearchResults, ValueCreate

class CRUDValue(CRUDBase [Value, ValueCreate, ValueSearchResults]):
    ...
value = CRUDValue(Value)

