from .base import CRUDBase
from gearbox.models import Value
from gearbox.schemas import ValueSearchResults, ValueCreate
from sqlalchemy.orm import Session
from sqlalchemy import func, update, select, exc

class CRUDValue(CRUDBase [Value, ValueCreate, ValueSearchResults]):

    async def get_value(self, 
                        current_session: Session, 
                        value_str: str, 
                        operator: str,
                        unit: str,
                        is_numeric: bool):
        stmt = select(Value).where(Value.value_string==value_str).where(Value.operator==operator).where(Value.unit==unit).where(Value.is_numeric==is_numeric)
        result = await current_session.execute(stmt)
        value = result.unique().scalars().first()
        return value

value_crud = CRUDValue(Value)

