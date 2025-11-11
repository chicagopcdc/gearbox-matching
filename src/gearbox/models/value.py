from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class Value(Base):
    __tablename__ = 'value'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    description = mapped_column(String, nullable=True)
    is_numeric = mapped_column(Boolean)
    value_string = mapped_column(String)
    unit_id = mapped_column(Integer, ForeignKey('unit.id', name='fk_value_unit_id'))
    operator = mapped_column(String)
    create_date = mapped_column(DateTime, nullable=True)
    active = mapped_column(Boolean, nullable=True)

    UniqueConstraint(is_numeric, unit_id, value_string, operator, name='value_num_unit_op_uix')

    el_criteria_has_criterions = relationship("ElCriteriaHasCriterion", back_populates="value")
    criteria = relationship("CriterionHasValue", back_populates="value")
    triggered_bys = relationship("TriggeredBy", back_populates="value")
    unit = relationship("Unit", back_populates="values", lazy="joined")
