from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt


class AlgorithmEngine(Base):
    __tablename__ = 'algorithm_engine'
    id = Column(Integer, primary_key=True, autoincrement=True)
    criterion_id = Column(Integer, ForeignKey('criterion.id'), nullable=True)
    parent_id = Column(Integer, nullable=True)
    parent_path = Column(String(45), nullable=True)
    operator = Column(String(45), nullable=True)

    study_versions = relationship("StudyAlgorithmEngine", back_populates="algorithm_engine")   
