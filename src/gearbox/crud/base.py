from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.sql import text
from sqlalchemy import update, select, exc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.dialects import postgresql
from gearbox.util import status
from sqlalchemy.orm import noload

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
            errors = ','.join([str(id) for id in ids_to_check if not await self.get(db, id=id)])
        else:
            errors = ids_to_check if not await self.get(db, id=ids_to_check) else None
        if errors:
            error_msg = f"ids: {errors} do not exist in {self.model.__name__}."
        return error_msg

    async def get( self, db: Session, id: int, active: bool = None, noload_rel: List[ModelType] = None ) -> ModelType:

        stmt = select(self.model).where(self.model.id == id)

        if active != None: 
            if 'active' not in self.model.__fields__.keys():
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{self.model.__tablename__} does not inlude 'active' attribute")        
            stmt = stmt.where(self.model.active == active)

        # exclude relationships from query
        if noload_rel:
            for noload_relationship in noload_rel:
                stmt = stmt.options(noload(noload_relationship))
            #stmt = stmt.options(noload(noload_rel))

        try:
            result_db = await db.execute(stmt)
            # not using scalar_one here because we don't necessarily
            # want to throw an error if we get more than one row here
            result = result_db.unique().scalars().first()
            return result
        except exc.SQLAlchemyError as e:
            logger.error(f"SQL ERROR IN base.get method: {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        

    async def get_multi( self, db: Session, active: bool = None, where: List[str] = None, noload_rel: List[ModelType] = None ) -> List[ModelType]:

        stmt = select(self.model)
        if active != None:
            cols = [str(c).split('.')[1] for c in self.model.__table__.columns]
            if 'active' in cols:
                stmt = stmt.where(self.model.active == active)
            else:
                logger.error(f"ERROR no 'active' attribute in model")
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{self.model.__tablename__} does not inlude 'active' attribute")        

        # enables querying on cols 
        if where:
            for w in where:
                stmt = stmt.where(text(w))

        # exclude relationships from query
        if noload_rel:
            for noload_relationships in noload_rel:
                stmt = stmt.options(noload(noload_relationships))
        try:
            result_db = await db.execute(statement=stmt)
            result = result_db.unique().scalars().all()
            return result

        except exc.SQLAlchemyError as e:
            logger.error(f"SQL ERROR IN base.get_multi method: {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        # set create_date here if not already set and it is in the schema

        if "create_date" in obj_in_data.keys():
            obj_in_data["create_date"] = datetime.now() if not obj_in_data["create_date"] else obj_in_data["create_date"]
        if "update_date" in obj_in_data.keys():
            obj_in_data["update_date"] = datetime.now() if not obj_in_data["update_date"] else obj_in_data["update_date"]
        if "start_date" in obj_in_data.keys():
            obj_in_data["start_date"] = datetime.now() if not obj_in_data["start_date"] else obj_in_data["start_date"]

        try:
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            await db.commit()
            return db_obj
        except IntegrityError as e:
            logger.error(f"CREATE CRUD IntegrityError ERROR {e}")
            raise HTTPException(status.HTTP_409_CONFLICT, f"INTEGRITY SQL ERROR: {type(e)}: {e}")
        except exc.SQLAlchemyError as e:
            logger.error(f"CREATE CRUD SQLAlchemyError ERROR {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        
        except Exception as e:
            logger.error(f"CREATE CRUD OTHER ERROR {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"OTHER ERROR: {type(e)}: {e}")        

    async def set_active_all_rows(self, db: Session, active_upd: bool) -> bool: 
        if not 'active' in self.model.__table__.columns.keys():
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{self.model.__tablename__} does not inlude 'active' attribute")        
        stmt = ( update(self.model)
            .values(active=active_upd)
        )
        res = await db.execute(stmt)
        await db.commit()
        return True

    async def set_active(self, db: Session, id: int, active: bool) -> ModelType: 
        
        if not 'active' in self.model.__table__.columns.keys():
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{self.model.__tablename__} does not inlude 'active' attribute")        

        upd_obj = await db.execute(select(self.model).where(self.model.id == id))

        if not upd_obj:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"id: {id} does not exist in {self.model.__tablename__}")        

        upd_obj.active = active
        await db.commit()

    async def update( self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            if "update_date" in obj_data.keys():
                obj_data["update_date"] = datetime.now()

            db.add(db_obj)
            await db.commit()
            return db_obj

        except IntegrityError as e:
            logger.error(f"INTEGREITY ERROR IN BASE UPDATE: {e}")
            raise HTTPException(status.HTTP_409_CONFLICT, f"INTEGRITY SQL ERROR: {type(e)}: {e}")
        except exc.SQLAlchemyError as e:
            logger.error(f"SQLALCHEMY ERROR IN BASE UPDATE: {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        
        except Exception as e:
            logger.error(f"OTHER ERROR IN BASE UPDATE: {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ERROR: {type(e)}: {e}")        

    def compile_query(self,query):
        compiler = query.compile if not hasattr(query, 'statement') else query.statement.compile
        return compiler(dialect=postgresql.dialect())


    async def upsert(self, db:Session, model: Type[ModelType], row, as_of_date_col='create_date', no_update_cols=[], constraint_cols=[]) -> ModelType:
        table = model.__table__

        stmt = insert(table).values(row)

        update_cols = [c.name for c in table.c
                   if c not in list(table.primary_key.columns)
                   and c.name not in no_update_cols]
        
        try:
            # Note - 'excluded' is a reference to the row that was not inserted due to conflict #
            if len(constraint_cols) > 0:
                on_conflict_stmt = stmt.on_conflict_do_update(
                    index_elements=constraint_cols,
                    set_={k: getattr(stmt.excluded, k) for k in update_cols},
                    index_where=(getattr(model, as_of_date_col) < getattr(stmt.excluded, as_of_date_col))
                ).returning(model)
            else:
                # if no constraint columns specified use primary key cols
                on_conflict_stmt = stmt.on_conflict_do_update(
                    index_elements=table.primary_key.columns,
                    set_={k: getattr(stmt.excluded, k) for k in update_cols},
                    index_where=(getattr(model, as_of_date_col) < getattr(stmt.excluded, as_of_date_col))
                ).returning(model)

            # Print the query for debugging
            retval = await db.execute(on_conflict_stmt)
            updated = retval.first()
            await db.commit()
            return updated
        
        except exc.SQLAlchemyError as e:
            logger.error(f"SQL ERROR IN UPSERT {type(e)} {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR IN UPSERT: {type(e)}: {e}")        
        except Exception as e:
            logger.error(f"ERROR IN UPSERT: {type(e)}: {e}") 
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ERROR IN UPSERT: {type(e)}: {e}")       
