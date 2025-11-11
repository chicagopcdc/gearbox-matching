from sqlalchemy import ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class SiteHasStudy(Base):
    __tablename__ = 'site_has_study'
    study_id = mapped_column(Integer, ForeignKey('study.id'), primary_key=True)
    site_id = mapped_column(Integer, ForeignKey('site.id'), primary_key=True)
    create_date = mapped_column("create_date", DateTime, nullable=True)
    active = mapped_column("active", Boolean, nullable=True)

    study = relationship("Study", back_populates="sites", lazy='joined')
    site = relationship("Site", back_populates="studies", lazy='joined',cascade="save-update, merge, delete, delete-orphan", single_parent=True)


