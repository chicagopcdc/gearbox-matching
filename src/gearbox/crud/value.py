from .base import CRUDBase
from gearbox.models import Value
from gearbox.schemas import ValueSearchResults, ValueCreate
from sqlalchemy.orm import Session
from sqlalchemy import func, update, select, exc

class CRUDValue(CRUDBase [Value, ValueCreate, ValueSearchResults]):

    async def get_value(self, 
                        db: Session, 
                        value_str: str, 
                        operator: str,
                        unit: str,
                        is_numeric: bool):
        print(f'IN CRUD 1')
        # stmt = select(Value).where(Value.value_string==value_str).where(Value.operator==operator).where(Value.unit==unit).where(Value.is_numeric==is_numeric)
        print(f"VALUE STR: {value_str} TYPE: {type(value_str)}")
        stmt = select(Value).where(Value.value_string == value_str)
        print(f'IN CRUD 2')
        result = await db.execute(stmt)
        print(f'IN CRUD 3')
        value = result.unique().scalars().first()
        print(f'IN CRUD 4')
        return value

value_crud = CRUDValue(Value)

