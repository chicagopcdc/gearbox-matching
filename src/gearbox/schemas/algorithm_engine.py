from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlgorithmEngine(BaseModel):
    id: int
    el_criteria_has_criterion_id: int
    parent_id: int
    parent_path: str
    operator: Optional[str]

    class Config:
        orm_mode = True

class AlgorithmEngineCreate(BaseModel):
    pass

class AlgorithmEngineSearchResults(BaseModel):
    pass
