from .base import CRUDBase
from gearbox.models import Value
from gearbox.schemas import ValueSearchResults, ValueCreate

class CRUDValue(CRUDBase [Value, ValueCreate, ValueSearchResults]):
    ...
value_crud = CRUDValue(Value)

