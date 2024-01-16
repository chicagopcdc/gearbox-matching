from .base import CRUDBase
from gearbox.models import Source
from gearbox.schemas import SourceCreate, SourceSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import select

class CRUDSource(CRUDBase [Source, SourceCreate, SourceSearchResults]):

    async def get_priority(self, db: Session, source: str) -> int: 
        stmt = select(Source.priority).where(Source.source == source)
        result = await db.execute(stmt)
        priority = result.scalars().first()
        return priority

source_crud = CRUDSource(Source)