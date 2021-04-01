from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from . import Base


class StudyLinks(Base):
    __tablename__ = "study_links"

    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey('study.id'))
    name = Column(String, nullable=True)
    href = Column(String, nullable=True)
    active = Column(Boolean, nullable=True)
