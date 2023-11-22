from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint, Text
from sqlalchemy.orm import relationship

from .base_class import Base 


class Study(Base):
    __tablename__ = "study"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    description = Column(String, nullable=True)
    create_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
    follow_up_info = Column(Text, nullable=True)

    UniqueConstraint(code, name='study_code_uix')

    patients = relationship('StudyHasPatient', back_populates='study', lazy='joined')
    sites = relationship("SiteHasStudy", back_populates="study", lazy='joined')
    # explicitly setting lazy='joined' here solved the problem of
    # pydantic trying to execute a join outside of the async 
    # program stream when lazy loading the study-links - this was happening even 
    # though joinedload is used in the query...
    # this only happens when trying to access via sites join to study
    # and not the other way around
    links = relationship("StudyLink", back_populates="study", lazy='joined')
    ext_ids = relationship("StudyExternalId", back_populates="study", lazy='joined')
    study_versions = relationship("StudyVersion", back_populates="study", lazy='joined')

    def __init__(self, name=None, code=None, description=None, active=None, create_date=None, sites=None, links=None, follow_up_info=None, ext_ids=None):
        self.name = name
        self.code = code
        self.description = description
        self.active = active
        self.create_date = create_date
        self.sites = []
        self.links = []
        self.follow_up_info = follow_up_info
        self.ext_ids = []
