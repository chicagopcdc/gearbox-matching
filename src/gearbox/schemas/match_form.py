from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional

class Group(BaseModel):
    id: int
    name: str

class MatchForm(BaseModel):
    groups: List[Group]

class MatchFormResponse(BaseModel):
    pass
