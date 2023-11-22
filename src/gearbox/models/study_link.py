from re import I
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from .base_class import Base


class StudyLink(Base):
    __tablename__ = "study_links"

    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey('study.id'))
    name = Column(String, nullable=True)
    href = Column(String)
    active = Column(Boolean, nullable=True)
    create_date = Column(DateTime, nullable=True)

    UniqueConstraint(study_id, href, name='study_link_uix')

    study = relationship("Study", back_populates="links")