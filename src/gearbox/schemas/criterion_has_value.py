from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, Optional
from gearbox.schemas import Value

class CriterionHasValueBase(BaseModel):
    criterion_id: int
    value_id: int
    create_date: Optional[datetime] = None

    class Config:
        from_attributes = True 

class CriterionHasValue(CriterionHasValueBase):
    pass

class CriterionHasValueValue(BaseModel):
    value: Optional[Value] = None

    class Config:
        from_attributes = True 

class CriterionHasValueCreate(CriterionHasValueBase):
    pass

class CriterionHasValueSearchResults(CriterionHasValueBase):
    results: Sequence[CriterionHasValue]
