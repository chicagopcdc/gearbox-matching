from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from .base_class import Base
from gearbox.util.types import CriterionStagingStatus

class CriterionStaging(Base):
    __tablename__ = 'criterion_staging'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id'), nullable=False)
    input_id = Column(String, nullable=True)
    code = Column(String)
    display_name = Column(String)
    description = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)
    status = Column(ENUM(CriterionStagingStatus), unique=False, nullable=False)

    ontology_code_id = Column(Integer, ForeignKey('ontology_code.id'), nullable=True)
    input_type_id = Column(Integer, ForeignKey('input_type.id'), nullable=True )

    start_char = Column(Integer)
    end_char = Column(Integer)
    text = Column(String, nullable=True)
    criterion_id = Column(Integer, ForeignKey('criterion.id'), nullable=True)

    #tags = relationship("CriterionHasTag", back_populates="criterion", lazy="joined")
    #el_criteria_has_criterions = relationship("ElCriteriaHasCriterion", back_populates="criterion", lazy="joined")
    #values = relationship("CriterionHasValue", back_populates="criterion", lazy="joined")
    # input_type = relationship("InputType", back_populates="criterions", lazy="joined")

    #display_rules = relationship("DisplayRules", back_populates="criterion", lazy="joined")
    #triggered_bys = relationship("TriggeredBy", back_populates="criterion", lazy="joined")