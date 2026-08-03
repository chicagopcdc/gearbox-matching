from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from fastapi.security import HTTPBearer
from fastapi import HTTPException 
from fastapi import status as fastapi_status
from sqlalchemy.orm import Session
from fastapi import Request, Depends 
from gearbox import config
from starlette.responses import JSONResponse
from typing import List
from gearbox import auth
from gearboxdatamodel.schemas import AlgorithmResponse
from gearbox import deps
from gearbox.services import match_conditions as mc
from gearboxdatamodel.util import status
from gearbox.util import bucket_utils
from gearbox.admin_login import admin_required, super_admin_required
from gearbox.util.bucket_utils import promote_object_to_prod
from gearbox.schemas import DeployProdDataResponse

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)


@mod.post("/deploy-prod-data", response_model=DeployProdDataResponse, dependencies=[ Depends(auth.authenticate), Depends(super_admin_required)], status_code=status.HTTP_200_OK)
async def deploy_prod_data(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    if not config.S3_PROD_BUCKET_NAME or not config.PROD_PROMOTION_ROLE_ARN:
        raise HTTPException(
            status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: production S3 promotion is not configured",
        )

    source_keys=[
        config.S3_BUCKET_MATCH_CONDITIONS_KEY_NAME, 
        config.S3_BUCKET_MATCH_FORM_KEY_NAME,
        config.S3_BUCKET_IMPORTANT_QUESTIONS_KEY_NAME,
        config.S3_BUCKET_STUDIES_KEY_NAME,
        config.S3_BUCKET_ELIGIBILITY_CRITERIA_KEY_NAME
    ]

    promote_object_to_prod(
        request=request,
        source_bucket=config.S3_BUCKET_NAME,
        source_keys=source_keys,
        dest_bucket=config.S3_PROD_BUCKET_NAME,
        prod_role_arn=config.PROD_PROMOTION_ROLE_ARN
    )

    return DeployProdDataResponse(
        status="success",
        source_bucket=config.S3_BUCKET_NAME,
        dest_bucket=config.S3_PROD_BUCKET_NAME,
        promoted_keys=source_keys,
    )

def init_app(app):
    app.include_router(mod, tags=["prod-deploy"])
