from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional

class SiteBase(BaseModel):
    name: str
    country: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    create_date: Optional[datetime] = None

    class Config:
        from_attributes = True 

class Site(SiteBase):
    id: int

class SiteCreate(SiteBase):
    pass

class SiteSearchResults(BaseModel):
    results: Sequence[Site]
