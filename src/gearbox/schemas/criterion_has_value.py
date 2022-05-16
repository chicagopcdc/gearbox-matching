from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional, Any
from pydantic.utils import GetterDict

class CriterionValueGetter(GetterDict):
    # map and reformat 'value' fields
    def get(self, key: str, default: Any = None) -> Any:
        if key in ('id','code','description','type','value_string','unit','operator','create_date','active','el_criteria_has_criterions'):
            # note 'value' is the table name here
            return getattr(self._obj.value, key)
        else:
            return super(CriterionValueGetter, self).get(key, default)

class CriterionValue(BaseModel):
    id: int
    code: Optional[str]
    description: Optional[str]
    type: Optional[str]
    value_string: Optional[str]
    unit: Optional[str]
    operator: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True
        getter_dict = CriterionValueGetter

