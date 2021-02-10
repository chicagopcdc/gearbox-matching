from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class ElCriteriaHasCriterion(Base):
    __tablename__ = 'el_criteria_has_criterion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    criterion_id = Column(Integer, ForeignKey('criterion.id'))
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id'))
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
    value_id = Column(Integer, ForeignKey('value.id'))

    eligibility_criteria = relationship("EligibilityCriteria", back_populates="criterions")
    criterion = relationship("Criterion", back_populates="eligibility_criterias")
    value = relationship("Value", back_populates="eligibility_criterias")
