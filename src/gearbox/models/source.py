from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from .base_class import Base


class Source(Base):
    __tablename__ = 'source'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String, nullable=True)
    priority = Column(Integer, nullable=True)

    UniqueConstraint(source, name='source_uix')

    studies = relationship("Study", back_populates="study_source")
    sites = relationship("Site", back_populates="site_source")


