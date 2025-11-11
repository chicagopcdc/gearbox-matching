import typing as t

from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    id: t.Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()