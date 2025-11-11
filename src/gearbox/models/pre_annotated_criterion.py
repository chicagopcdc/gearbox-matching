from sqlalchemy import ForeignKey, Integer, Boolean, String
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class PreAnnotatedCriterion(Base):
    __tablename__ = "pre_annotated_criterion"

    id = mapped_column(Integer, primary_key=True)
    raw_criteria_id = mapped_column(Integer, ForeignKey('raw_criteria.id'))
    text = mapped_column(String)
    label = mapped_column(String, nullable=True)
    is_standard_gb_var = mapped_column(Boolean, nullable=True)

    raw_criteria = relationship("RawCriteria", back_populates="pre_annotated_criteria")
    pre_annotated_criterion_models = relationship("PreAnnotatedCriterionModel", 
        back_populates="pre_annotated_criterion", 
        cascade="all, delete-orphan, delete")
