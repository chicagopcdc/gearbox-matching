from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional
from .criterion_tag import CriterionTag
from .criterion_value import CriterionValue

class CriterionBase(BaseModel):
    code: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    create_date: Optional[datetime] = None
    active: Optional[bool] = None
    ontology_code_id: Optional[int] = None
    input_type_id: int

    class Config:
        orm_mode = True

class Criterion(CriterionBase):
    id: int
    tags: Optional[List[CriterionTag]] = None
    values: Optional[List[CriterionValue]] = None

class CriterionCreate(CriterionBase):
    pass

class CriterionPublish(CriterionBase):
    criterion_staging_id: int
    code: str
    display_name: str
    description: str
    create_date: Optional[datetime] = None
    active: Optional[bool] = None
    ontology_code_id: Optional[int] = None
    input_type_id: int
    values: Optional[List[int]] = None

class CriterionCreateIn(CriterionBase):
    code: str
    tags: List[int]
    values: Optional[List[int]] = None
    display_rules_priority: int
    display_rules_version: Optional[int] = None
    triggered_by_criterion_id: Optional[int] = None
    triggered_by_value_id: Optional[int] = None
    triggered_by_path: Optional[str] = None
    criterion_staging_id: Optional[int] = None


class CriterionSearchResults(BaseModel):
    results: Sequence[Criterion]    