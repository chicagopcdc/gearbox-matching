from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt

class Study_Algorithm_Engine(Base):
    __tablename__ = 'study_algorithm_engine'

    __table_args__ = {'extend_existing': True}
    
    study_version_id = Column(Integer, ForeignKey('study_version.id'), primary_key=True)
    algorithm_engine_id = Column(Integer, ForeignKey('algorithm_engine.id'), primary_key=True)
    study_id = Column(Integer, ForeignKey('study.id'), primary_key=True)
    start_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
