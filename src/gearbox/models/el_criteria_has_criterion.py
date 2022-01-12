from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship, backref

from .base_class import Base

class ElCriteriaHasCriterion(Base):
    __tablename__ = 'el_criteria_has_criterion'
    id = Column(Integer, primary_key=True, autoincrement=True)

    criterion_id = Column(Integer, ForeignKey('criterion.id'))
    criterion = relationship("Criterion", backref=backref("el_criteria_has_criterions"))

    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id'))
    eligibility_criteria = relationship("EligibilityCriteria", backref=backref("el_criteria_has_criterions"))

    value_id = Column(Integer, ForeignKey('value.id'))
    value = relationship("Value", backref=backref("el_criteria_has_criterions"))

    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
    
    
