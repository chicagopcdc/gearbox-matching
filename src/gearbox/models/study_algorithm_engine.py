from sqlalchemy import ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class StudyAlgorithmEngine(Base):
    __tablename__ = 'study_algorithm_engine'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    start_date = mapped_column(DateTime, nullable=True)
    algorithm_logic = mapped_column(JSON)

    class Config:
        orm_mode = True  

    study_version = relationship("StudyVersion", back_populates="study_algorithm_engine")
