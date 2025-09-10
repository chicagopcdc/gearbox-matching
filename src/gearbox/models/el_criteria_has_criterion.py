from sqlalchemy import ForeignKey, Integer, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class ElCriteriaHasCriterion(Base):
    __tablename__ = 'el_criteria_has_criterion'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    criterion_id = mapped_column(Integer, ForeignKey('criterion.id'))
    eligibility_criteria_id = mapped_column(Integer, ForeignKey('eligibility_criteria.id'))
    create_date = mapped_column(DateTime, nullable=True)
    active = mapped_column(Boolean, nullable=True)
    value_id = mapped_column(Integer, ForeignKey('value.id'))

    UniqueConstraint(criterion_id, eligibility_criteria_id, value_id, name='el_criteria_has_criterion_uix')

    eligibility_criteria = relationship("EligibilityCriteria", back_populates="el_criteria_has_criterions", lazy="joined")
    criterion = relationship("Criterion", back_populates="el_criteria_has_criterions", lazy="joined")
    value = relationship("Value", back_populates="el_criteria_has_criterions", lazy="joined")
