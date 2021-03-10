from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base


class InputTypeHasValue(Base):
    __tablename__ = 'input_type_has_value'
    value_id = Column(Integer, ForeignKey('value.id'))
    input_type_id = Column(Integer, primary_key=True, ForeignKey('input_type.id'))
    create_date = Column(DateTime, nullable=True)
