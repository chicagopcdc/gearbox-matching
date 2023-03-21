from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from .base_class import Base


class ElCriteriaHasCriterion(Base):
    __tablename__ = 'el_criteria_has_criterion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    criterion_id = Column(Integer, ForeignKey('criterion.id'))
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id'))
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
    value_id = Column(Integer, ForeignKey('value.id'))

    UniqueConstraint(criterion_id, eligibility_criteria_id, value_id, name='el_criteria_has_criterion_uix')

    eligibility_criteria = relationship("EligibilityCriteria", back_populates="el_criteria_has_criterions", lazy="joined")
    criterion = relationship("Criterion", back_populates="el_criteria_has_criterions", lazy="joined")
    value = relationship("Value", back_populates="el_criteria_has_criterions", lazy="joined")
    #eligibility_criteria = relationship("EligibilityCriteria", back_populates="el_criteria_has_criterion", lazy="joined")
    #criterion = relationship("Criterion", back_populates="el_criteria_has_criterion", lazy="joined")
    #value = relationship("Value", back_populates="el_criteria_has_criterion", lazy="joined")

