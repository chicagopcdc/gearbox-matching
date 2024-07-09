from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from authutils.token.fastapi import access_token
from fastapi import HTTPException, APIRouter
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from . import logger
from gearbox.util import status
from typing import List

from gearbox.schemas import SavedInputSearchResults, SavedInputCreate 
from gearbox.services import user_input as user_input_service
from gearbox import deps
from gearbox import auth 
from gearbox.admin_login import admin_required
from gearbox import config
mod = APIRouter()


@mod.get("/user-input/validation-update", status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def get_object_latest(
    request: Request,
    session: Session = Depends(deps.get_session),
):
    """
        reset cache of criteria data for validating user input.

        Args:
            request (Request): starlette request (which contains reference to FastAPI app)
            token (HTTPAuthorizationCredentials, optional): bearer token
        
        returns:
            200: "user_validation data cleared"
            4xx-5xx: if there is in error with collecting data from DB
    """
    await user_input_service.reset_user_validation_data()

    return "user_validation data cleared"



@mod.post("/user-input", response_model=SavedInputSearchResults, status_code=status.HTTP_200_OK,dependencies=[ Depends(auth.authenticate)])
async def save_object(
    body: SavedInputCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    """
        Save user form input, return saved object list to the user.

        Args:
            body (UploadSavedInput): input body for saving input
            request (Request): starlette request (which contains reference to FastAPI app)
            token (HTTPAuthorizationCredentials, optional): bearer token
    """
    #validate here
    await user_input_service.validate_user_input(session, body.data)
    saved_user_input = await user_input_service.create_saved_input(session=session, user_input=body, user_id=int(user_id))
    return saved_user_input

@mod.get("/user-input/latest", response_model=SavedInputSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_object_latest(
    request: Request,
    session: Session = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    """
    Attempt to fetch the latest version of the user saved search, 
    return the saved object.

    Args:
        request (Request): starlette request (which contains reference to FastAPI app)
        token (HTTPAuthorizationCredentials, optional): bearer token

    Returns:
        200: { "results": [{id: 1, "value": ""}] }
        404: if the obj is not found
    """
    saved_user_input = await user_input_service.get_latest_user_input(session=session, user_id=int(user_id))
    return saved_user_input

# get all saved inputs for a user
@mod.get("/user-input/all", response_model=List[SavedInputSearchResults], status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_object_all(
    request: Request,
    session: Session = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    """
    Attempt to fetch all saved inputs for the user, 
    return the saved object.

    Args:
        request (Request): starlette request (which contains reference to FastAPI app)
        token (HTTPAuthorizationCredentials, optional): bearer token

    Returns:
        200: { "user": user_id, "results": [{id: 1, "value": ""}...] }
        404: if the obj is not found
    """
    # check that the environment variable ENABLE_PHI from the config.py is set to True

    if not config.ENABLE_PHI:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"this endpoint is not active")

    
    saved_user_input = await user_input_service.get_all_user_input(session=session, user_id=int(user_id))
    
    return saved_user_input

def init_app(app):
    app.include_router(mod, tags=["user-input"])
