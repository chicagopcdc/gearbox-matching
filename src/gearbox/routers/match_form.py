import pprint
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
from ..schemas import DisplayRules 
from ..crud.match_form import get_form_info
from .. import deps
from ..util.bounds import bounds

mod = APIRouter()

@mod.get("/match-form", response_model=List[DisplayRules], status_code=HTTP_200_OK)
async def get_match_info(
    request: Request,
    session: Session = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    auth_header = str(request.headers.get("Authorization", ""))
    form_info = await get_form_info(session)

    G = []
    F = []

    for display_rules in form_info:
        criterion_dict = {}
        for ctag in display_rules.criterion.tags:
            g = {
                'id': ctag.tag.id,
                'name': ctag.tag.code
            }
            G.append(g)

        logger.info(f"BOUNDS KEYS: {bounds.keys()}")
        if display_rules.active:
            criterion_dict = {'id': display_rules.criterion_id}
            for ctag in display_rules.criterion.tags:
                criterion_dict.update({'groupId': ctag.tag.id})
            if display_rules.criterion.active:
                code = display_rules.criterion.code
                criterion_dict.update({'name': code})
                logger.info(f"CODE: {code}")
                # N O T E: criterion.code is null, so need to update 
                # to create some test data
                if code in bounds.keys():
                    criterion_dict.update({code: bounds[code]})
                criterion_dict.update({'label':display_rules.criterion.display_name})
                criterion_dict.update({'type':display_rules.criterion.input_type.render_type})

                for tb in display_rules.triggered_bys:
                    if tb.active:
                        pass #N O T E - start here Tuesday...



        logger.info(f"CRITERION_DICT {criterion_dict}") 

    return form_info

def init_app(app):
    app.include_router(mod, tags=["match_form"])