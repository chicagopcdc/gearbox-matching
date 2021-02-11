from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

from app.main.model.criterion_has_tag import CriterionHasTag

# , flask_bcrypt                                                                                                                                                                                             

class Criterion(Base):
    __tablename__ = 'criterion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, nullable=True)
    display_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
    ontology_code_id = Column(Integer, ForeignKey('ontology_code.id'))
    input_type_id = Column(Integer, ForeignKey('input_type.id'))

    tags = relationship("CriterionHasTag", back_populates="criterion")
    eligibility_criterias = relationship("ElCriteriaHasCriterion", back_populates="criterion")
