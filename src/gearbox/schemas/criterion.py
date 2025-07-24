from pydantic import BaseModel, model_serializer
from datetime import datetime
from typing import Sequence, List, Optional
from .criterion_has_tag import CriterionHasTagTag
from .criterion_has_value import CriterionHasValueValue

class CriterionBase(BaseModel):
    code: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    create_date: Optional[datetime] = None
    active: Optional[bool] = None
    ontology_code_id: Optional[int] = None
    input_type_id: int

    class Config:
        from_attributes = True 

class Criterion(CriterionBase):
    id: int
    tags: Optional[List[CriterionHasTagTag]] = None
    values: Optional[List[CriterionHasValueValue]] = None

    # The purpose of this function is to flatten
    # sites into the format expected for the studies extract
    @model_serializer
    def serialize_model(self):

        return {
            'code': self.code,
            'display_name': self.display_name,
            'description': self.description,
            'create_date': self.create_date,
            'active': self.active,
            'ontology_code_id': self.ontology_code_id,
            'input_type_id': self.input_type_id,
            'tags': self.tags,
            'values': self.values
        }

    class Config:
        from_attributes = True 

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
