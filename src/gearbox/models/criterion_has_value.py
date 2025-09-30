from sqlalchemy import ForeignKey, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class CriterionHasValue(Base):
    __tablename__ = 'criterion_has_value'
    criterion_id = mapped_column(Integer, ForeignKey('criterion.id'), primary_key=True)
    value_id = mapped_column(Integer, ForeignKey('value.id'), primary_key=True)
    create_date = mapped_column("create_date",DateTime, nullable=True)

    criterion = relationship("Criterion", back_populates="values")
    value = relationship("Value", back_populates="criteria", lazy="joined")
