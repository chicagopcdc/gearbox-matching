import sre_compile
from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional

class InputTypeBase(BaseModel):
    id: int
    data_type: Optional[str]
    render_type: Optional[str]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True

class InputType(InputTypeBase):
    id: int

class InputTypeCreate(InputTypeBase):
    pass

class InputTypeSearchResults(BaseModel):
    results: Sequence[InputType]
