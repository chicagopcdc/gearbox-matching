from __future__ import annotations
import json
from jsonschema import validate
from pydantic import BaseModel, ValidationError, validator, Json
from datetime import datetime
from typing import Optional, List, Sequence, Any
import jsonschema

class AlgorithmResponse(BaseModel):
    operator: str
    criteria: int
    algorithm: List[AlgorithmResponse]

class AlgorithmEngine(BaseModel):
    pass

AlgorithmResponse.update_forward_refs()