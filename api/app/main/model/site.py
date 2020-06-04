from app.main import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
# , flask_bcrypt


class SiteHasStudy(db.Model):
    __tablename__ = 'site_has_study'
    study_id = db.Column(db.Integer, ForeignKey('study.id'), primary_key=True)
    site_id = db.Column(db.Integer, ForeignKey('site.id'), primary_key=True)
    create_date = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, nullable=True)
    study = relationship("Study", back_populates="sites")
    site = relationship("Site", back_populates="studies")



class Site(db.Model):
    __tablename__ = 'site'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=True)
    code = db.Column(db.String(45), nullable=True)
    create_date = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, nullable=True)


    studies = relationship("SiteHasStudy", back_populates="site")

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}