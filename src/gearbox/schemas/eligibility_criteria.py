from re import I
from pydantic import BaseModel, Extra
from datetime import datetime
from typing import Optional, Sequence

class EligibilityCriteriaBase(BaseModel):
    create_date: Optional[datetime]

    class Config:
        orm_mode = True   

class EligibilityCriteria(EligibilityCriteriaBase):
    id: int

class EligibilityCriteriaCreate(EligibilityCriteriaBase):
    pass

class EligibilityCriteriaSearchResults(BaseModel):
    results: Sequence[EligibilityCriteria]    