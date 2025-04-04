from sqlalchemy import ForeignKey, Column, Integer, Boolean, String
from sqlalchemy.orm import relationship

from .base_class import Base


class PreAnnotatedCriterion(Base):
    __tablename__ = "pre_annotated_criterion"

    id = Column(Integer, primary_key=True)
    raw_criteria_id = Column(Integer, ForeignKey('raw_criteria.id'))
    text = Column(String)
    label = Column(String, nullable=True)
    is_standard_gb_var = Column(Boolean, nullable=True)

    raw_criteria = relationship("RawCriteria", back_populates="pre_annotated_criteria")
    pre_annotated_criterion_models = relationship("PreAnnotatedCriterionModel", back_populates="pre_annotated_criterion", cascade="all,delete")
