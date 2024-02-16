from .base import CRUDBase
from gearbox.models import Unit
from gearbox.schemas import UnitCreate, UnitSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import func, update, select, exc

class CRUDUnit(CRUDBase [Unit, UnitCreate, UnitSearchResults]):
    ...
    async def get_unit(self, current_session: Session, unit_name: str):
        print(f"CRUD METHOD 1")
        stmt = select(Unit).where(Unit.name == unit_name)
        print(f"CRUD METHOD 2: {stmt}")
        result = await current_session.execute(stmt)
        print(f"CRUD METHOD 3")
        unit = result.unique().scalars().first()
        return unit

unit_crud = CRUDUnit(Unit)