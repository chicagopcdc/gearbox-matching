from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base_class import Base


class Value(Base):
    __tablename__ = 'value'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=True)
    is_numeric = Column(Boolean)
    value_string = Column(String)
    unit_id = Column(Integer, ForeignKey('unit.id', name='fk_value_unit_id'))
    operator = Column(String)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    UniqueConstraint(is_numeric, unit_id, value_string, operator, name='value_num_unit_op_uix')

    el_criteria_has_criterions = relationship("ElCriteriaHasCriterion", back_populates="value")
    criteria = relationship("CriterionHasValue", back_populates="value")
    triggered_bys = relationship("TriggeredBy", back_populates="value")
    unit = relationship("Unit", back_populates="values", lazy="joined")