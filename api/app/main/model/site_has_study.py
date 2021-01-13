from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt


class SiteHasStudy(Base):
    __tablename__ = 'site_has_study'
    study_id = Column(Integer, ForeignKey('study.id'), primary_key=True)
    site_id = Column(Integer, ForeignKey('site.id'), primary_key=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    study = relationship("Study", back_populates="sites")
    site = relationship("Site", back_populates="studies")

