from .base import CRUDBase
from gearbox.models import InputType
from gearbox.schemas import InputTypeSearchResults, InputTypeCreate

class CRUDInputType(CRUDBase [InputType, InputTypeCreate, InputTypeSearchResults]):
    ...
input_type_crud = CRUDInputType(InputType)