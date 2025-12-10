from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from fastapi.security import HTTPBearer
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
from gearbox.utils.bucket_util import promote_object_to_prod
from gearbox.schemas import DeployProdDataResponse

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)


@mod.post("/deploy-prod-data", response_model=DeployProdDataResponse, dependencies=[ Depends(auth.authenticate), Depends(super_admin_required)], status_code=status.HTTP_200_OK)
async def deploy_prod_data(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    promote_object_to_prod(
        request=request,
        source_bucket=config.STAGING_BUCKET,
        source_keys=["current/state.json"],
        dest_bucket=config.PROD_BUCKET,
        prod_role_arn=config.PROD_PROMOTION_ROLE_ARN
    )

    return DeployProdDataResponse(
        status="success",
        source_bucket=config.STAGING_BUCKET,
        dest_bucket=config.PROD_BUCKET,
        promoted_keys=source_keys,
    )

def init_app(app):
    app.include_router(mod, tags=["prod-deploy"])
