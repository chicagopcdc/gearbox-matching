from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, load_only
from sqlalchemy import func, update, select, exc
from sqlalchemy.exc import IntegrityError
from gearbox.util import status

from datetime import datetime

# from app.db.base_class import Base
from ..models import Base

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
        error_msg = None
        if isinstance(ids_to_check, list):
            errors = '.'.join([str(id) for id in ids_to_check if not await self.get(db, id)])
        else:
            errors = ids_to_check if not await self.get(db,ids_to_check) else None
        if errors:
            error_msg = f"ids: {errors} do not exist in {self.model}."
        return error_msg

    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        try:
            result_db = await db.execute(stmt)
            result = result_db.scalars().first()
            return result
        except exc.SQLAlchemyError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        

    async def get_multi( self, db: Session, *, where: str=None, load_only: str=None, skip: int = 0, limit: int = 5000) -> List[ModelType]:
        # stmt_str = "select(self.model)"
        # stmt = stmt_str
        # CONSTRUCT WHERE (if param exists) USING EVAL TO CREATE THE STATEMENT
        stmt_str = "select(self.model)"
        stmt_str += f".where({where})" if where else stmt_str 
        stmt_str += f".load_only({load_only})" if load_only else stmt_str
        stmt = eval(stmt_str)
        try:
            result_db = await db.execute(stmt)
            result = result_db.unique().scalars().all()
            return result
        except exc.SQLAlchemyError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        # set create_date here if not already set and it is in the schema
        if "create_date" in obj_in_data.keys():
            obj_in_data["create_date"] = datetime.now() if not obj_in_data["create_date"] else obj_in_data["create_date"]
        db_obj = self.model(**obj_in_data)  # type: ignore
        try:
            db.add(db_obj)
            await db.commit()
            return db_obj
        except IntegrityError as e:
            raise HTTPException(status.HTTP_409_CONFLICT, f"INTEGRITY SQL ERROR: {type(e)}: {e}")
        except exc.SQLAlchemyError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        

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