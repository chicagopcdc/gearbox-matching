from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.main import DbSession
from app.main.model.algorithm_engine import StudyAlgorithmEngine
# , flask_bcrypt

Base = declarative_base()


class StudyVersion(Base):
    """ User Model for storing user related details """
    __tablename__ = "study_version"

    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey('study.id'), primary_key=True) 
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    #algorithm_engines = relationship("StudyAlgorithmEngine", back_populates="study_version")
    #study = relationship("Study", back_populates="study_versions")

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
