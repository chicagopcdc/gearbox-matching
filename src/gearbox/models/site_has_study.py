from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from .base_class import Base


class SiteHasStudy(Base):
    __tablename__ = 'site_has_study'
    study_id = Column(Integer, ForeignKey('study.id'), primary_key=True)
    site_id = Column(Integer, ForeignKey('site.id'), primary_key=True)
    create_date = Column("create_date", DateTime, nullable=True)
    active = Column("active", Boolean, nullable=True)

    study = relationship("Study", back_populates="sites", lazy='joined')
    site = relationship("Site", back_populates="studies", lazy='joined')


