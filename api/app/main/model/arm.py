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


    # @property
    # def password(self):
    #     raise AttributeError('password: write-only field')

    # @password.setter
    # def password(self, password):
    #     self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    # def check_password(self, password):
    #     return flask_bcrypt.check_password_hash(self.password_hash, password)

    # def __repr__(self):
    #     return "<User '{}'>".format(self.username)