from __future__ import annotations
from pydantic import BaseModel 
from typing import List

class AlgorithmResponse(BaseModel):
    operator: str
    criteria: int
    algorithm: List[AlgorithmResponse]