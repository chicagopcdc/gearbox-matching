from .base import CRUDBase
from gearbox.models import Value, Unit
from gearbox.schemas import ValueSearchResults, ValueCreate
from sqlalchemy.orm import Session
from sqlalchemy import func, update, select, exc, subquery


class CRUDValue(CRUDBase [Value, ValueCreate, ValueSearchResults]):

    # This query is used to check if a value exists in the db. It is used to
    # make sure no duplicate values are created. 
    # TO DO: replace this with a unique constraint on
    # value_str, operator, unit (name, id?), is_numeric??
    async def get_value(self, 
                        db: Session, 
                        value_str: str, 
                        operator: str,
                        unit_name: str,
                        is_numeric: bool):

        unit_subq = select(Unit).where(Unit.name==unit_name).subquery()
        stmt = select(Value).where(Value.value_string == value_str).\
                where(Value.operator == operator).\
                where(Value.is_numeric == is_numeric).\
                join(unit_subq, Value.unit_id == unit_subq.c.id)
        result = await db.execute(stmt)
        value = result.unique().scalars().first()
        return value
    
    async def get_value_by_value_string(self, db: Session, value_str: str):
        stmt = select(Value).where(Value.value_string == value_str)
        result = await db.execute(stmt)
        value = result.unique().scalars().first()
        return value

value_crud = CRUDValue(Value)

