from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from .base_class import Base


class Value(Base):
    __tablename__ = 'value'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type = Column(String, nullable=True)
    value_string = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    operator = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    UniqueConstraint(code, name='value_code_uix')
    UniqueConstraint(type, unit, value_string, operator, name='value_code_unit_uix')

    el_criteria_has_criterions = relationship("ElCriteriaHasCriterion", back_populates="value")
    criteria = relationship("CriterionHasValue", back_populates="value")
    triggered_bys = relationship("TriggeredBy", back_populates="value")
