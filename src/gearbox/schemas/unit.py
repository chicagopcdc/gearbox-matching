import sre_compile
from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional

class UnitBase(BaseModel):
    name: str

    class Config:
        from_attributes = True 

class Unit(UnitBase):
    id: int

class UnitCreate(UnitBase):
    pass

class UnitSearchResults(BaseModel):
    results: Sequence[Unit]
