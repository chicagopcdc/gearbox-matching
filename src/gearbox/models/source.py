from sqlalchemy import Integer, String, DateTime, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class Source(Base):
    __tablename__ = 'source'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    source = mapped_column(String, nullable=True)
    priority = mapped_column(Integer, nullable=False)

    UniqueConstraint(source, name='source_uix')
    UniqueConstraint(priority, name='priority_uix')

    studies = relationship("Study", back_populates="study_source")
    sites = relationship("Site", back_populates="site_source")


