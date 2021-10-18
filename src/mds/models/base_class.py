# import typing as t

# from sqlalchemy.ext.declarative import as_declarative, declared_attr
# same as Base = declarative_base()
# class_registry: t.Dict = {}

# @as_declarative(class_registry=class_registry)
# class Base:
#     id: t.Any
#     __name__: str

#     # Generate __tablename__ automatically
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()


from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()