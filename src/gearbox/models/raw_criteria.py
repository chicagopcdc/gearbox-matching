from sqlalchemy import ForeignKey, Integer, UniqueConstraint, DateTime, String
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.dialects.postgresql import JSON

from .base_class import Base


class RawCriteria(Base):
    __tablename__ = "raw_criteria"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    eligibility_criteria_id = mapped_column(Integer, ForeignKey('eligibility_criteria.id'))
    input_id = mapped_column(String, nullable=True)
    data = mapped_column(JSON)
    create_date = mapped_column(DateTime, nullable=True)

    UniqueConstraint(eligibility_criteria_id, name='raw_criteria_uix')

    eligibility_criteria = relationship("EligibilityCriteria", back_populates="raw_criteria")
    pre_annotated_criteria = relationship("PreAnnotatedCriterion", back_populates="raw_criteria")