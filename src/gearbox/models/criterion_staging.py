from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.types import ARRAY
from .base_class import Base
from gearbox.util.types import AdjudicationStatus,  EchcAdjudicationStatus

class CriterionStaging(Base):
    __tablename__ = 'criterion_staging'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id'), nullable=False)
    input_id = Column(String, nullable=True)
    code = Column(String, nullable=True)
    display_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)
    criterion_adjudication_status = Column(ENUM(AdjudicationStatus), unique=False, nullable=False)
    echc_adjudication_status= Column(ENUM(EchcAdjudicationStatus), unique=False, nullable=False)
    
    last_updated_by_user_id=Column(Integer, nullable=True)

    ontology_code_id = Column(Integer, ForeignKey('ontology_code.id'), nullable=True)
    input_type_id = Column(Integer, ForeignKey('input_type.id'), nullable=True )

    start_char = Column(Integer)
    end_char = Column(Integer)
    text = Column(String, nullable=True)
    criterion_id = Column(Integer, ForeignKey('criterion.id'), nullable=True)

    criterion_value_ids = Column(ARRAY(Integer), nullable=True)
    echc_value_ids= Column(ARRAY(Integer), nullable=True)
    echc_ids= Column(ARRAY(Integer), nullable=True)