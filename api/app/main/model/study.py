from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.main import DbSession

# , flask_bcrypt


Base = declarative_base()


class Study(Base):
    """ User Model for storing user related details """
    __tablename__ = "study"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=True)
    code = Column(String(45), nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    #sites = relationship("SiteHasStudy", back_populates="study")
    #study_versions = relationship("StudyVersion", back_populates="study")

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
