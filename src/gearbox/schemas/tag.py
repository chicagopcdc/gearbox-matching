import sre_compile
from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional

class TagBase(BaseModel):
    code: str
    type: Optional[str]

    class Config:
        orm_mode = True

class Tag(TagBase):
    id: int

class TagCreate(TagBase):
    pass

class TagSearchResults(BaseModel):
    results: Sequence[Tag]
