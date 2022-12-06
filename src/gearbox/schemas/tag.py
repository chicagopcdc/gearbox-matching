from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional

class Tag(BaseModel):
    id: Optional[int]
    code: Optional[str]
    type: Optional[str]

    class Config:
        orm_mode = True


class TagCreate(BaseModel):
    pass

class TagSearchResults(BaseModel):
    pass
