from sqlalchemy import ForeignKey, Integer, String, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.types import ARRAY, Enum as SQLEnum
from .base_class import Base
from gearbox.util.types import AdjudicationStatus,  EchcAdjudicationStatus

class CriterionStaging(Base):
    __tablename__ = 'criterion_staging'
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    eligibility_criteria_id = mapped_column(Integer, ForeignKey('eligibility_criteria.id'), nullable=False)
    code = mapped_column(String, nullable=True)
    display_name = mapped_column(String, nullable=True)
    description = mapped_column(String, nullable=True)
    create_date = mapped_column(DateTime, nullable=True)
    criterion_adjudication_status : Mapped[AdjudicationStatus] = mapped_column(SQLEnum(AdjudicationStatus))
    echc_adjudication_status : Mapped[EchcAdjudicationStatus] = mapped_column(SQLEnum(EchcAdjudicationStatus))
    
    last_updated_by_user_id=mapped_column(Integer, nullable=True)

    ontology_code_id = mapped_column(Integer, ForeignKey('ontology_code.id'), nullable=True)
    input_type_id = mapped_column(Integer, ForeignKey('input_type.id'), nullable=True )

    start_char = mapped_column(Integer)
    end_char = mapped_column(Integer)
    text = mapped_column(String, nullable=True)
    criterion_id = mapped_column(Integer, ForeignKey('criterion.id'), nullable=True)

    criterion_value_ids = mapped_column(ARRAY(Integer), nullable=True)
    echc_value_ids= mapped_column(ARRAY(Integer), nullable=True)
    echc_ids= mapped_column(ARRAY(Integer), nullable=True)
