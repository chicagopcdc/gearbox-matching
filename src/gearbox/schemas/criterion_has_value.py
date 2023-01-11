from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict

class CriterionHasValueBase(BaseModel):
    criterion_id: int
    value_id: int
    assoc_create_date: Optional[datetime]

    class Config:
        orm_mode = True

class CriterionHasValue(CriterionHasValueBase):
    pass

class CriterionHasValueCreate(CriterionHasValueBase):
    pass

class CriterionHasValueSearchResults(CriterionHasValueBase):
    results: Sequence[CriterionHasValue]
