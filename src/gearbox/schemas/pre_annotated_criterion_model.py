import sre_compile
from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional

class PreAnnotatedCriterionModelBase(BaseModel):
    id: int
    pre_annotated_criterion_id: int
    model: Optional[str]

    class Config:
        from_attributes = True 

class PreAnnotatedCriterionModel(PreAnnotatedCriterionModelBase):
    pass

class PreAnnotatedCriterionModelCreate(BaseModel):
    pre_annotated_criterion_id: int
    model: Optional[str]

class PreAnnotatedCriterionModelSearchResults(BaseModel):
    results: Sequence[PreAnnotatedCriterionModel]
