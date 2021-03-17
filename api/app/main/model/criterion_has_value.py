from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base


class CriterionHasValue(Base):
    __tablename__ = 'criterion_has_value'
    criterion_id = Column(Integer, ForeignKey('criterion.id'), primary_key=True)
    value_id = Column(Integer, ForeignKey('value.id'))
    create_date = Column(DateTime, nullable=True)

    criterion = relationship("Criterion", back_populates="values")
    value = relationship("Value", back_populates="criteria")
