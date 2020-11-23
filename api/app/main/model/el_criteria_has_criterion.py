from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class ElCriteriaHasCriterion(Base):
    __tablename__ = 'el_criteria_has_criterion'
    criterion_id = Column(Integer, ForeignKey('criterion.id'), primary_key=True)
    eligibility_criteria_id = Column(Integer, ForeignKey('eligibility_criteria.id'), primary_key=True)
    code = Column(String(45), nullable=True)
    display_name = Column(String(45), nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
