from sqlalchemy import Integer, Text, DateTime
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class Login(Base):
    """ Login User Model for storing login-related details """
    __tablename__ = "logins"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    sub_id = mapped_column(Text, primary_key=True)
    refresh_token = mapped_column(Text, nullable=False)
    iat = mapped_column(DateTime, nullable=True)
    exp = mapped_column(DateTime, nullable=True)
