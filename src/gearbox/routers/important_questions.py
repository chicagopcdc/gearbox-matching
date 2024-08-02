from gearbox import config
from fastapi import APIRouter
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import Request, Depends
from fastapi.security import HTTPBearer
from starlette.responses import JSONResponse
from gearbox import auth
from gearbox import deps
from gearbox.util import status, bucket_utils


mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/important-questions", dependencies=[ Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_match_form(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    params = []
    presigned_url = bucket_utils.get_presigned_url(request, config.S3_BUCKET_IMPORTANT_QUESTIONS_KEY_NAME, params, "get_object")
    return JSONResponse(presigned_url, status.HTTP_200_OK)