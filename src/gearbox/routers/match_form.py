import json
from datetime import date
from time import gmtime, strftime
from fastapi import APIRouter
from fastapi import HTTPException, APIRouter, Security
from sqlalchemy.orm import Session
from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
from .. import auth
from ..schemas import DisplayRules 
from ..crud.match_form import get_form_info
from .. import deps
from ..util.bounds import bounds

import logging
logger = logging.getLogger('gb-logger')

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/match-form", response_model=List[DisplayRules], status_code=HTTP_200_OK)
async def get_match_info(
    request: Request,
    session: Session = Depends(deps.get_session),
    token: HTTPAuthorizationCredentials = Security(bearer)
):
    auth_header = str(request.headers.get("Authorization", ""))
    user_id = await auth.authenticate_user(token)
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
            # get unique groups 
            G = list({v['id']:v for v in G}.values())
            G = sorted(G, key = lambda i: i['id'])

        if display_rules.active:
            criterion_dict = {'id': display_rules.criterion_id}
            for ctag in display_rules.criterion.tags:
                criterion_dict.update({'groupId': ctag.tag.id})
            if display_rules.criterion.active:
                code = display_rules.criterion.code
                criterion_dict.update({'name': code})
                # N O T E: criterion.code is null, so need to update 
                # to create some test data
                if code in bounds.keys():
                    criterion_dict.update(bounds[code])

                criterion_dict.update({'label':display_rules.criterion.description})
                criterion_dict.update({'type':display_rules.criterion.input_type.render_type})

                # showIf logic
                showIf = {
                    'operator': 'OR', #Tom's code says: "always OR as scripted for now"
                    'criteria': []
                }
                for tb in display_rules.triggered_bys:
                    if tb.active:
                        if tb.value.active:
                            op = tb.value.operator
                            vs = tb.value.value_string
                            cid = tb.criterion_id
                        # else return empty dict??
                            try:
                                crits = showIf.get('criteria')
                                new_crit = {
                                    'id': cid,
                                    'operator:': op,
                                    'value': eval(vs)
                                }
                                crits.append(new_crit)
                                showIf.update(({'criteria': crits}))
                            except Exception as e:
                                logger.error(e)

                # end showIf logic
                if showIf.get('criteria'):
                    criterion_dict.update({'showIf':showIf})

                options = []
                if len(display_rules.criterion.values) > 1:
                    if display_rules.criterion.input_type.render_type == 'select':
                        criterion_dict.update({'placeholder': 'Select'})
                        chvalues = [x for x in display_rules.criterion.values]
                        for chvalue in chvalues:
                            o = {'value': chvalue.value.id}
                            o.update({'label':chvalue.value.code})
                            options.append(o)
                    if display_rules.criterion.input_type.render_type == 'radio':
                        chvalues = [x for x in display_rules.criterion.values]
                        for chvalue in chvalues:
                            o = {'value': chvalue.value.id}
                            o.update({'label': chvalue.value.value_string})
                            o.update({'description': ""})
                            options.append(o)
                if len(options) > 0:
                    criterion_dict.update({'options': options})
        F.append(criterion_dict)

        body = {"groups": G, "fields": F}
        response = {
            "current_date": date.today().strftime("%B %d, %Y"),
            "current_time": strftime("%H:%M:%S +0000", gmtime()),
            "status": "OK",
            "body": body
        }
    return JSONResponse(response, HTTP_200_OK)


def init_app(app):
    app.include_router(mod, tags=["match_form"])
