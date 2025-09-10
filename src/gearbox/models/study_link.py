from re import I
from sqlalchemy import ForeignKey, Integer, String, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class StudyLink(Base):
    __tablename__ = "study_links"

    id = mapped_column(Integer, primary_key=True)
    study_id = mapped_column(Integer, ForeignKey('study.id'))
    name = mapped_column(String, nullable=True)
    href = mapped_column(String)
    active = mapped_column(Boolean, nullable=True)
    create_date = mapped_column(DateTime, nullable=True)

    UniqueConstraint(study_id, href, name='study_link_uix')

    study = relationship("Study", back_populates="links")
