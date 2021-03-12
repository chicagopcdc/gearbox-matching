from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base


class InputTypeHasValue(Base):
    __tablename__ = 'input_type_has_value'
    value_id = Column(Integer, ForeignKey('value.id'))
    input_type_id = Column(Integer, ForeignKey('input_type.id'), primary_key=True)
    create_date = Column(DateTime, nullable=True)

    value = relationship("Value", back_populates="input_types")
    input_type = relationship("InputType", back_populates="values")
