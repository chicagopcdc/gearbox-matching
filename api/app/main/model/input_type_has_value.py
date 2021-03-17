from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base


class InputTypeHasValue(Base):
    __tablename__ = 'input_type_has_value'
    value_id = Column(Integer, ForeignKey('value.id'))
    criterion_id = Column(Integer, ForeignKey('criterion.id'), primary_key=True)
    create_date = Column(DateTime, nullable=True)

    criterion = relationship("Criterion", back_populates="values")
    value = relationship("Value", back_populates="criteria")
