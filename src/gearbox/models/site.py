from sqlalchemy import Integer, String, DateTime, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class Site(Base):
    __tablename__ = 'site'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=True)
    country = mapped_column(String, nullable=True)
    city = mapped_column(String, nullable=True)
    state = mapped_column(String, nullable=True)
    zip = mapped_column(String, nullable=True)
    create_date = mapped_column(DateTime, nullable=True)
    source_id = mapped_column(Integer, ForeignKey('source.id', name='fk_site_source_id'))

    UniqueConstraint(name, zip, name='site_uix')

    studies = relationship("SiteHasStudy", back_populates="site")
    site_source = relationship("Source", back_populates="sites",lazy='joined')

