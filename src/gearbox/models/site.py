from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from .base_class import Base


class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)
    source_id = Column(Integer, ForeignKey('source.id', name='fk_site_source_id'))

    UniqueConstraint(name, zip, name='site_uix')

    studies = relationship("SiteHasStudy", back_populates="site")
    site_source = relationship("Source", back_populates="sites",lazy='joined')

