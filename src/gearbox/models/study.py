from sqlalchemy import Integer, String, DateTime, Boolean, UniqueConstraint, Text, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base 


class Study(Base):
    __tablename__ = "study"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False)
    code = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=True)
    create_date = mapped_column(DateTime, nullable=True)
    active = mapped_column(Boolean, nullable=True)
    follow_up_info = mapped_column(Text, nullable=True)
    source_id = mapped_column(Integer, ForeignKey('source.id', name='fk_study_source_id'))

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
    study_source = relationship("Source", back_populates="studies",lazy='joined')

    def __init__(self, name=None, code=None, description=None, active=None, create_date=None, sites=None, links=None, follow_up_info=None, ext_ids=None, source_id=None):
        self.name = name
        self.code = code
        self.description = description
        self.active = active
        self.create_date = create_date
        self.sites = []
        self.links = []
        self.follow_up_info = follow_up_info
        self.ext_ids = []
        self.source_id = source_id
