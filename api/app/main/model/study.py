from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession
from app.main.model.site import SiteHasStudy
from app.main.model.study_version import StudyVersion

# , flask_bcrypt


class Study(Base):
    __tablename__ = "study"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=True)
    code = Column(String(45), nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    sites = relationship("SiteHasStudy", back_populates="study")
    study_versions = relationship("StudyVersion", back_populates="study")
