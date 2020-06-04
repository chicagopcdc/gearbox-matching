from sqlalchemy.orm import relationship

from app.main import db
from app.main.model.site import SiteHasStudy
from app.main.model.study_version import StudyVersion

# , flask_bcrypt

class Study(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "study"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=True)
    code = db.Column(db.String(45), nullable=True)
    create_date = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, nullable=True)

    sites = relationship("SiteHasStudy", back_populates="study")
    study_versions = relationship("StudyVersion", back_populates="study")

    def as_dict(self):
       # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}




# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     children = relationship("Child", back_populates="parent")

# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
#     parent_id = Column(Integer, ForeignKey('parent.id'))
#     parent = relationship("Parent", back_populates="children")