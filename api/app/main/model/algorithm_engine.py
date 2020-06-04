from app.main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
# , flask_bcrypt


class StudyAlgorithmEngine(db.Model):
    __tablename__ = 'study_algorithm_engine'
    study_id = db.Column(db.Integer, ForeignKey('study.id'), primary_key=True)
    study_version_id = db.Column(db.Integer, ForeignKey('study_version.id'), primary_key=True)
    algorithm_engine_id = db.Column(db.Integer, ForeignKey('algorithm_engine.id'), primary_key=True)
    start_date = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, nullable=True)
    
    study_version = relationship("StudyVersion", back_populates="algorithm_engines")
    algorithm_engine = relationship("AlgorithmEngine", back_populates="study_versions")



class AlgorithmEngine(db.Model):
    __tablename__ = 'algorithm_engine'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=True)
    version = db.Column(db.String(45), nullable=True)
    link = db.Column(db.String(256), nullable=True)
    description = db.Column(db.String(512), nullable=True)
    function = db.Column(db.String(512), nullable=True)
    type = db.Column(db.String(45), nullable=True)
    create_date = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, nullable=True)

    study_versions = relationship("StudyAlgorithmEngine", back_populates="algorithm_engine")

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}