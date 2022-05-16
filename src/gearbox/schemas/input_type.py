import sre_compile
from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional

class InputType(BaseModel):
    id: int
    data_type: Optional[str]
    render_type: Optional[str]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True

class InputTypeCreate(BaseModel):
    pass

class InputTypeSearchResults(BaseModel):
    pass
