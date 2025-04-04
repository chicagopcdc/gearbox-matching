from sqlalchemy import ForeignKey, Column, Integer, UniqueConstraint, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from .base_class import Base


class RawCriteria(Base):
    __tablename__ = "raw_criteria"

    id = Column(Integer, primary_key=True)
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id'))
    input_id = Column(String, nullable=True)
    data = Column(JSON)
    create_date = Column(DateTime, nullable=True)

    UniqueConstraint(eligibility_criteria_id, name='raw_criteria_uix')

    eligibility_criteria = relationship("EligibilityCriteria", back_populates="raw_criteria")
    pre_annotated_criteria = relationship("PreAnnotatedCriterion", back_populates="raw_criteria")