from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict

class CriterionHasTagBase(BaseModel):
    criterion_id: int
    tag_id: int

    class Config:
        orm_mode = True

class CriterionHasTag(CriterionHasTagBase):
    pass

class CriterionHasTagCreate(CriterionHasTagBase):
    pass

class CriterionHasTagSearchResults(CriterionHasTagBase):
    results: Sequence[CriterionHasTag]
