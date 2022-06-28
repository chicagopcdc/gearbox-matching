from re import I
from datetime import date
from time import gmtime, strftime
from fastapi import APIRouter, HTTPException
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from fastapi import Request, Depends
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
from ..schemas import EligibilityCriteriaResponse
from ..crud.eligibility_criteria import get_eligibility_criteria
from .. import deps

import logging
logger = logging.getLogger('gb-logger')

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/eligibility-criteria", response_model=List[EligibilityCriteriaResponse], dependencies=[Depends(auth.authenticate)], status_code=HTTP_200_OK)
async def get_ec(
    request: Request,
    session: Session = Depends(deps.get_session),
):
    results = await get_eligibility_criteria(session)

    body = []
    try:
        if results:
            for echc in results:
                if echc.active == True:
                    the_id = echc.id
                    value_id = echc.value_id
                    fieldId = echc.criterion_id
                    the_value = echc.value
                    operator = the_value.operator
                    render_type = echc.criterion.input_type.render_type
                    if render_type in ['radio','select']:
                        fieldValue = value_id
                    elif render_type in ['age']:
                        unit = the_value.unit
                        if unit in ['years']:
                            fieldValue = eval(the_value.value_string)
                        else:
                            if unit == 'months':
                                fieldValue = round(eval(the_value.value_string)/12.0)
                            elif unit == 'days':
                                fieldValue = round(eval(the_value.value_string)/365.0)
                    else:
                        fieldValue = eval(the_value.value_string)

                    f = {
                        'id': the_id,
                        'fieldId': fieldId,
                        'fieldValue': fieldValue,
                        'operator': operator
                    }
                    body.append(f)
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
    app.include_router(mod, tags=["eligibility_criteria"])
