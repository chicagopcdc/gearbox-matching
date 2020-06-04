from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from app.main import db
from app.main.model.algorithm_engine import StudyAlgorithmEngine

# , flask_bcrypt

class StudyVersion(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "study_version"

    id = db.Column(db.Integer, primary_key=True)
    study_id = db.Column(db.Integer, ForeignKey('study.id'), primary_key=True) 
    create_date = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, nullable=True)

    algorithm_engines = relationship("StudyAlgorithmEngine", back_populates="study_version")
    study = relationship("Study", back_populates="study_versions")

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}




