from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import func, update, select, exc
from sqlalchemy.exc import IntegrityError
from gearbox.util import status

from datetime import datetime
from ..models import *

from cdislogging import get_logger
logger = get_logger(__name__)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model


    async def check_key(self, db:Session, ids_to_check: Union[List[int], int]):
        """
        method checks if a key or list of keys exist
        """
        error_msg = None
        if isinstance(ids_to_check, list):
            errors = '.'.join([str(id) for id in ids_to_check if not await self.get(db, id=id)])
        else:
            errors = ids_to_check if not await self.get(db, id=ids_to_check) else None
        if errors:
            error_msg = f"ids: {errors} do not exist in {self.model}."
        return error_msg

    async def get( self, db: Session, id: int, active: bool = None ) -> ModelType:

        stmt = select(self.model).where(self.model.id == id)

        if active != None: 
            if 'active' not in self.model.__fields__.keys():
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{self.model.__tablename__} does not inlude 'active' attribute")        
            stmt = stmt.where(self.model.active == active)

        # add where if active
        try:
            result_db = await db.execute(stmt)
            # not using scalar_one here because we don't necessarily
            # want to throw an error if we get more than one row here
            result = result_db.unique().scalars().first()
            #if not result:
            #    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"No 'active' rows in {self.model.__tablename__} ")        
            return result
        except exc.SQLAlchemyError as e:
            logger.error(f"SQL ERROR IN base.get method: {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        

    async def get_multi( self, db: Session, active: bool = None, where: List[str] = None ) -> List[ModelType]:

        stmt = select(self.model)
        if active != None:
            print(f"SELF MODEL: {self.model}")
            print(f"SELF MODEL TYPE: {type(self.model)}")
            print(f"MODEL COLUMNS: {self.model.__table__.columns}")
            cols = [str(c).split('.')[1] for c in self.model.__table__.columns]
            if 'active' in cols:
                stmt = stmt.where(self.model.active == active)
            else:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{self.model.__tablename__} does not inlude 'active' attribute")        
        
        if where:
            for w in where:
                stmt = stmt.where(text(w))

        try:
            print(f"STATEMENT: {stmt}")
            result_db = await db.execute(stmt)
            result = result_db.unique().scalars().all()
            #if not result:
            #    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"No 'active' rows in {self.model.__tablename__} ")        
            return result

        except exc.SQLAlchemyError as e:
            print(f"SQL ERROR IN base.get method: {e}")
            logger.error(f"SQL ERROR IN base.get method: {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        # set create_date here if not already set and it is in the schema
        if "create_date" in obj_in_data.keys():
            obj_in_data["create_date"] = datetime.now() if not obj_in_data["create_date"] else obj_in_data["create_date"]
        db_obj = self.model(**obj_in_data)
        try:
            db.add(db_obj)
            # await db.commit()
            await db.flush()
            return db_obj
        except IntegrityError as e:
            logger.error(f"CREATE CRUD IntegrityError ERROR {e}")
            raise HTTPException(status.HTTP_409_CONFLICT, f"INTEGRITY SQL ERROR: {type(e)}: {e}")
        except exc.SQLAlchemyError as e:
            logger.error(f"CREATE CRUD SQLAlchemyError ERROR {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        

    async def set_active(self, db: Session, id: int, active: bool) -> ModelType: 
        # update object to set status 'active'
        # raise error if 'active' not an attribute
        # raise error if object with id does not exist
        # update 'active' T if F, F if T
        if not 'active' in self.model.__fields__.keys():
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{self.model.__tablename__} does not inlude 'active' attribute")        

        upd_obj = db.execute(select (self.model)).where(self.model.id == id)
        if not upd_obj:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"id: {id} does not exist in {self.model.__tablename__}")        

        upd_obj.active = active
        db.flush()

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        try:
            db.add(db_obj)
            await db.commit()
            return db_obj
        except IntegrityError as e:
            raise HTTPException(status.HTTP_409_CONFLICT, f"INTEGRITY SQL ERROR: {type(e)}: {e}")
        except exc.SQLAlchemyError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        

    """
    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
    """