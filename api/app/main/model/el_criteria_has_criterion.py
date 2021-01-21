from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base


class ElCriteriaHasCriterion(Base):
    __tablename__ = 'el_criteria_has_criterion'
    criterion_id = Column(Integer, ForeignKey('criterion.id'), primary_key=True)
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id'), primary_key=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
    value_id = Column(Integer, ForeignKey('value.id'), nullable=True)

    eligibility_criteria = relationship("EligibilityCriteria", back_populates="criterions")
    criterion = relationship("Criterion", back_populates="eligibility_criterias")
    value = relationship("Value", back_populates="eligibility_criterias")
