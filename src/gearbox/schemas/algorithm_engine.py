from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AlgorithmResponse(BaseModel):
    operator: str
    criteria: int
    algorithm: List[AlgorithmResponse]

class AlgorithmEngine(BaseModel):
    pass

AlgorithmResponse.update_forward_refs()