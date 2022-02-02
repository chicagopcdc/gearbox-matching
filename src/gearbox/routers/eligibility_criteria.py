from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Request, Depends
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
from .. import logger, auth
from ..schemas import ElCriterionHasCriterionSchema
from ..crud.eligibility_criteria import get_eligibility_criteria
from .. import deps

mod = APIRouter()

@mod.get("/eligibility-criteria", response_model=List[ElCriterionHasCriterionSchema], status_code=HTTP_200_OK)
async def get_ec(
    request: Request,
    session: Session = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    auth_header = str(request.headers.get("Authorization", ""))
    results = await get_eligibility_criteria(session)
    return results

def init_app(app):
    app.include_router(mod, tags=["eligibility_criteria"])