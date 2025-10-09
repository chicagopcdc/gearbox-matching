from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Sequence, List, Any, Optional

class SiteBase(BaseModel):
    name: str
    country: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    create_date: Optional[datetime] = None
    location_lat:  Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=8)
    location_long:  Optional[Decimal] = Field(default=None, max_digits=11, decimal_places=8)

    class Config:
        from_attributes = True 

class Site(SiteBase):
    id: int

class SiteCreate(SiteBase):
    pass

class SiteSearchResults(BaseModel):
    results: Sequence[Site]
