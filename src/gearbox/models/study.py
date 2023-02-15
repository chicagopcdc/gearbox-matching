from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from .base_class import Base


class Study(Base):
    __tablename__ = "study"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    code = Column(String, nullable=True)
    description = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)

    UniqueConstraint(code, name='study_code_uix')

    sites = relationship("SiteHasStudy", back_populates="study")
    # explicitly setting lazy='joined' here solved the problem of
    # pydantic trying to execute a join outside of the async 
    # program stream when lazy loading the study-links - this was happening even 
    # though joinedload is used in the query...
    # this only happens when trying to access via sites join to study
    # and not the other way around
    links = relationship("StudyLink", back_populates="study", lazy='joined')
