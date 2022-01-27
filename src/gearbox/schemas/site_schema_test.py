from pydantic import BaseModel
from datetime import datetime

class SiteSchemaTest(BaseModel):
    id: int
    name: str
    code: str
    create_date: datetime
    active: bool