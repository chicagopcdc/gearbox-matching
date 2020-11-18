from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class EligibilityCriteria(Base):
    __tablename__ = 'eligibility_criteria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    arm_id = Column(Integer, ForeignKey('arm.id'))
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
