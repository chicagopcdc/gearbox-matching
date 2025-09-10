from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref, mapped_column

from .base_class import Base


class PreAnnotatedCriterionModel(Base):
    __tablename__ = "pre_annotated_criterion_model"

    id = mapped_column(Integer, primary_key=True)
    pre_annotated_criterion_id = mapped_column(Integer, ForeignKey('pre_annotated_criterion.id', ondelete="CASCADE"))
    model = mapped_column(String)
    
    pre_annotated_criterion = relationship("PreAnnotatedCriterion", 
        back_populates="pre_annotated_criterion_models")
