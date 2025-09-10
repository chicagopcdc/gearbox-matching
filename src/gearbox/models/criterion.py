from sqlalchemy import ForeignKey, Integer, String, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.dialects.postgresql import ENUM
from .base_class import Base


class Criterion(Base):
    __tablename__ = 'criterion'
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    code = mapped_column(String)
    display_name = mapped_column(String)
    description = mapped_column(String, nullable=True)
    create_date = mapped_column(DateTime, nullable=True)
    active = mapped_column(Boolean, nullable=True)
    ontology_code_id = mapped_column(Integer, ForeignKey('ontology_code.id'), nullable=True)
    input_type_id = mapped_column(Integer, ForeignKey('input_type.id') )

    UniqueConstraint(code, name='criterion_code_uix')
    UniqueConstraint(display_name, name='criterion_display_name_uix')

    tags = relationship("CriterionHasTag", back_populates="criterion", lazy="joined",cascade="save-update, merge, delete,delete-orphan")
    el_criteria_has_criterions = relationship("ElCriteriaHasCriterion", back_populates="criterion", lazy="joined")
    values = relationship("CriterionHasValue", back_populates="criterion", lazy="joined")
    input_type = relationship("InputType", back_populates="criterions", lazy="joined")

    display_rules = relationship("DisplayRules", back_populates="criterion", lazy="joined")
    triggered_bys = relationship("TriggeredBy", back_populates="criterion", lazy="joined")
