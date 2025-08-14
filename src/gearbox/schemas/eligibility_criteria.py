from re import I
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Sequence
from gearbox.util.types import EligibilityCriteriaStatus

class EligibilityCriteriaBase(BaseModel):
    create_date: Optional[datetime] = None
    status: Optional[EligibilityCriteriaStatus] = None

    class Config:
        from_attributes = True 

class EligibilityCriteria(EligibilityCriteriaBase):
    id: int

class EligibilityCriteriaCreate(EligibilityCriteriaBase):
    pass

class EligibilityCriteriaSearchResults(BaseModel):
    results: Sequence[EligibilityCriteria]    
