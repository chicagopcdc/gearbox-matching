import sre_compile
from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional

class SourceBase(BaseModel):
    source: str
    priority: int

    class Config:
        from_attributes = True 

class Source(SourceBase):
    id: int

class SourceCreate(SourceBase):
    pass

class SourceSearchResults(BaseModel):
    results: Sequence[Source]
