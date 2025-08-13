from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref

from .base_class import Base


class PreAnnotatedCriterionModel(Base):
    __tablename__ = "pre_annotated_criterion_model"

    id = Column(Integer, primary_key=True)
    pre_annotated_criterion_id = Column(Integer, ForeignKey('pre_annotated_criterion.id'))
    model = Column(String)
    
    pre_annotated_criterion = relationship("PreAnnotatedCriterion", 
        back_populates="pre_annotated_criterion_models")
