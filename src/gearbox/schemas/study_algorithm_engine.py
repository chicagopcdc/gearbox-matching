from __future__ import annotations
from jsonschema import validate
from pydantic import BaseModel, Json
from datetime import datetime
from typing import Optional, List, Sequence, Any, Dict, Union

from enum import Enum

from gearbox.models import study_algorithm_engine

class OperatorEnum(str, Enum):
    op_and = "AND"
    op_or = "OR"

class AlgorithmLogic(BaseModel):
    operator: OperatorEnum
    criteria: List[Union['AlgorithmLogic',int]]

    def get_dict(self)->Json:
        return self.model_dump()

class StudyAlgorithmEngineBase(BaseModel):
    start_date: datetime | None = None
    algorithm_logic: Dict[Any, Any]

class StudyAlgorithmEngineIn(BaseModel):
    start_date: datetime | None = None
    algorithm_logic: AlgorithmLogic

class StudyAlgorithmEngineSave(StudyAlgorithmEngineBase):
    pass

class StudyAlgorithmEngine(StudyAlgorithmEngineBase):
    id: int

class StudyAlgorithmEngineCreate(StudyAlgorithmEngineIn):
    study_version_id: int

class StudyAlgorithmEngineUpdate(StudyAlgorithmEngineIn):
    study_version_id: int
    id: int

class StudyAlgorithmEngineSearchResults(BaseModel):
    results: Sequence[StudyAlgorithmEngine]    
