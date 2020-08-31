from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship

from . import Base
from app.main import DbSession

# , flask_bcrypt


class Login(Base):
    """ Login User Model for storing login-related details """
    __tablename__ = "logins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_id = Column(Text, primary_key=True)
    refresh_token = Column(Text, nullable=False)
    iat = Column(DateTime, nullable=True)
    exp = Column(DateTime, nullable=True)
