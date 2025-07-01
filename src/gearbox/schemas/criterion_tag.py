from pydantic import BaseModel
from typing import Sequence, Any, Optional
from pydantic.utils import GetterDict

class CriterionTagGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in ('id','code','type'):
            return getattr(self._obj.tag, key)
        else:
            return super(CriterionTagGetter, self).get(key, default)

class CriterionTag(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    type: Optional[str] = None

    class Config:
        orm_mode = True
        getter_dict = CriterionTagGetter

class CriterionHasTagCreate(CriterionTag):
    pass

class CriterionHasTagSearchResults(CriterionTag):
    results: Sequence[CriterionTag]
