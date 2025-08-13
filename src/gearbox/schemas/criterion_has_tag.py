from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from gearbox.schemas.tag import Tag

class CriterionHasTagBase(BaseModel):
    criterion_id: int
    tag_id: int
    tag: Optional[Tag] = None

    def __repr__(self):
        return f"<criterion_id={self.criterion_id}, tag_id={self.tag_id}"

    class Config:
        from_attributes = True        

class CriterionHasTag(CriterionHasTagBase):
    pass

class CriterionHasTagTag(BaseModel):
    tag: Optional[Tag] = None

    class Config:
        from_attributes = True 


class CriterionHasTagCreate(CriterionHasTagBase):
    pass

class CriterionHasTagSearchResults(CriterionHasTagBase):
    results: Sequence[CriterionHasTag]
