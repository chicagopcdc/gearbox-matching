from fastapi import APIRouter
from datetime import date
from time import gmtime, strftime
from sqlalchemy.orm import Session
from fastapi import Request, Depends, HTTPException
from starlette.responses import JSONResponse
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
from ..schemas import AlgorithmEngine
from ..crud.algorithm_engine import get_match_conditions
from .. import deps
from ..util import match_conditions as mc

mod = APIRouter()

@mod.get("/match-conditions", response_model=List[AlgorithmEngine], status_code=HTTP_200_OK)
async def get_site(
    request: Request,
    session: Session = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    auth_header = str(request.headers.get("Authorization", ""))
    all_algo_engs = await get_match_conditions(session)
    try:
        if all_algo_engs:
            pps = [x.parent_path for x in all_algo_engs]
            ops = [x.operator for x in all_algo_engs]
            #append another fake OR to trigger the final row to go in
            pps.append('terminus')
            ops.append('OR')

            full_paths = mc.get_full_paths(pps, ops)
            X = mc.merged(full_paths)
            R = mc.format(X)
            C = mc.cleanup(R)

            body = C
        else:
            body = []

        response = {
                "current_date": date.today().strftime("%B %d, %Y"),
                "current_time": strftime("%H:%M:%S +0000", gmtime()),
                "status": "OK",
                "body": body
        }
        return JSONResponse(response, HTTP_200_OK)
    except Exception as exc:
        logger.error(exc, exc_info=True)
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            f"Could not verify, parse, and/or validate scope from provided access token.",
        )


def init_app(app):
    app.include_router(mod, tags=["match_conditions"])