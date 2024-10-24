from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from .base_class import Base


class Criterion(Base):
    __tablename__ = 'criterion'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String)
    display_name = Column(String)
    description = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
    ontology_code_id = Column(Integer, ForeignKey('ontology_code.id'), nullable=True)
    input_type_id = Column(Integer, ForeignKey('input_type.id') )

    UniqueConstraint(code, name='criterion_code_uix')
    UniqueConstraint(display_name, name='criterion_display_name_uix')

    tags = relationship("CriterionHasTag", back_populates="criterion", lazy="joined")
    el_criteria_has_criterions = relationship("ElCriteriaHasCriterion", back_populates="criterion", lazy="joined")
    values = relationship("CriterionHasValue", back_populates="criterion", lazy="joined")
    input_type = relationship("InputType", back_populates="criterions", lazy="joined")

    display_rules = relationship("DisplayRules", back_populates="criterion", lazy="joined")
    triggered_bys = relationship("TriggeredBy", back_populates="criterion", lazy="joined")
