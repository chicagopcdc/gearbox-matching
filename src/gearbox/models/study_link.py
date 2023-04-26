from re import I
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .base_class import Base


class StudyLink(Base):
    __tablename__ = "study_links"

    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey('study.id'))
    name = Column(String, nullable=True)
    href = Column(String)
    active = Column(Boolean, nullable=True)

    study = relationship("Study", back_populates="links")