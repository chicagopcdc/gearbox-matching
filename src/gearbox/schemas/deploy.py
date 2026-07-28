from pydantic import BaseModel
from typing import List

class DeployProdDataResponse(BaseModel):
    status: str
    source_bucket: str
    dest_bucket: str
    promoted_keys: List[str]
