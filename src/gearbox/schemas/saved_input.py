from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional



class SavedInputBase(BaseModel):
    user_id: int
    name: Optional[str] = None
    patient_id: Optional[int] = None
    data: List[dict]
    create_date: Optional[datetime] = None
    update_date: Optional[datetime] = None


# properties in DB
class SavedInputDB(SavedInputBase):
    id: int
    create_date: datetime
    update_date: datetime

    class Config:
        from_attributes = True 

# properties to return to client
class SavedInput(SavedInputDB):
    pass


class SavedInputSearchResults(BaseModel):
    results: List[dict]
    id: int
    name: Optional[str] = None

class SavedInputCreate(BaseModel):
    data: List[dict]
    id: Optional[int] = None
    name: Optional[str] = None

class SavedInputPost(SavedInputBase):
    id: Optional[int] = None
    pass
