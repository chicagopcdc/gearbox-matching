from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship, backref

from .base_class import Base

class SiteHasStudy(Base):
    __tablename__ = 'site_has_study'

    study_id = Column(Integer, ForeignKey('study.id'), primary_key=True)
    study = relationship("Study", backref=backref("sites"))

    site_id = Column(Integer, ForeignKey('site.id'), primary_key=True)
    site = relationship("Site", backref=backref("studies"))

    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
