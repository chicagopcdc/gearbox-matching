from main import db

class Arm(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "arm"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    version_id = db.Column(db.Integer, nullable=False)
    study_id = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(45), nullable=True)
    create_date = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)


    