from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Request, Depends
from fastapi import APIRouter, Security
from fastapi.security import HTTPBearer 
from . import logger
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from typing import List
from .. import auth
from ..schemas import Value
from ..crud.criterion_value import get_values
from .. import deps

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/values", response_model=List[Value], dependencies=[Depends(auth.authenticate)], status_code=HTTP_200_OK)
async def get_all_values(
    request: Request,
    session: Session = Depends(deps.get_session),
):
    results = await get_values(session)

    for x in results:
        logger.info(f"TYPE X: {type(x)}")
        logger.info(f"x.id {x.id}")

    return results

def init_app(app):
    app.include_router(mod, tags=["criterion_value"])
