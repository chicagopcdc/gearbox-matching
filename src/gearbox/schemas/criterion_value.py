from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional, Any
from pydantic.utils import GetterDict

class CriterionValueGetter(GetterDict):
    # map and reformat 'value' fields
    def get(self, key: str, default: Any = None) -> Any:
        if key in ('id','description','value_string','operator','create_date','active','is_numeric','unit_id'):
            # note 'value' is the table name here
            return getattr(self._obj.value, key)
        else:
            return super(CriterionValueGetter, self).get(key, default)

class CriterionValue(BaseModel):
    id: int
    description: Optional[str]
    type: Optional[str]
    value_string: Optional[str]
    unit_name: Optional[str]
    operator: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True
        getter_dict = CriterionValueGetter
