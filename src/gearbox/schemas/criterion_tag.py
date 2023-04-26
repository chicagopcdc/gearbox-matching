from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict

class CriterionTagGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in ('id','code','type'):
            return getattr(self._obj.tag, key)
        else:
            return super(CriterionTagGetter, self).get(key, default)

class CriterionTag(BaseModel):
    id: Optional[int]
    code: Optional[str]
    type: Optional[str]

    class Config:
        orm_mode = True
        getter_dict = CriterionTagGetter

class CriterionHasTagCreate(CriterionTag):
    pass

class CriterionHasTagSearchResults(CriterionTag):
    results: Sequence[CriterionTag]
