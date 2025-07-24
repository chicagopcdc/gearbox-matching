#import sre_compile
from pydantic import BaseModel
from typing import Sequence, Optional

class TagBase(BaseModel):
    code: str
    type: Optional[str] = None

    class Config:
        from_attributes = True 

class Tag(TagBase):
    id: int

class TagCreate(TagBase):
    pass

class TagSearchResults(BaseModel):
    results: Sequence[Tag]
