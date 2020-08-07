from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.main import DbSession
#from app.main.model.study_version import StudyVersion
#from app.main.model.study import Study
# , flask_bcrypt


Base = declarative_base()

class SiteHasStudy(Base):
    __tablename__ = 'site_has_study'
    study_id = Column(Integer, ForeignKey('study.id'), primary_key=True)
    site_id = Column(Integer, ForeignKey('site.id'), primary_key=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    #study = relationship("Study", back_populates="sites")
    #site = relationship("Site", back_populates="studies")


class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=True)
    code = Column(String(45), nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    #studies = relationship("SiteHasStudy", back_populates="site")

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
   
