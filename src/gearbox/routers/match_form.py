import json
import re
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
from ..util import match_conditions as mc

import logging
logger = logging.getLogger('gb-logger')

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

def update_dict(d, critlookup):
    for key in d:
        if key == 'criteria':
            if isinstance(d[key], list):
                for i in range(0, len(d[key])):
                    if not isinstance(d[key][i], dict):
                        try:
                            d[key][i] = critlookup[int(d[key][i])] 
                        except KeyError:
                            logger.error("Error message about improperly configured path - path ids do not exist for this...")

                    else: 
                        update_dict(d[key][i], critlookup)
    return d

@mod.get("/match-form", response_model=List[DisplayRules], dependencies=[Depends(auth.authenticate)], status_code=HTTP_200_OK)
async def get_match_info(
    request: Request,
    session: Session = Depends(deps.get_session),
):
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
            print(f"APPENDING FOR: {display_rules.criterion_id}")
            for ctag in display_rules.criterion.tags:
                if ctag.tag.type == 'form':
                    criterion_dict.update({'groupId': ctag.tag.id})
            if display_rules.criterion.active:
                code = display_rules.criterion.code
                criterion_dict.update({'name': code})
                if code in bounds.keys():
                    criterion_dict.update(bounds[code])

                criterion_dict.update({'label':display_rules.criterion.description})
                criterion_dict.update({'type':display_rules.criterion.input_type.render_type})

                print(f"DISPLAY RULES ID: {display_rules.criterion.id}")
                print(f"DISPLAY RULES DATA TYPE: {display_rules.criterion.input_type.data_type.upper()}")
                if display_rules.criterion.input_type.data_type.upper() == 'INTEGER':
                    criterion_dict.update({'min' : 0})
                if display_rules.criterion.input_type.data_type.upper() == 'FLOAT':
                    criterion_dict.update({'min' : 0})
                    criterion_dict.update({'step' : 0.1})
                if display_rules.criterion.input_type.data_type.upper() == 'PERCENTAGE':
                    criterion_dict.update({'min' : 0})
                    criterion_dict.update({'max' : 100})
                    criterion_dict.update({'step' : 0.1})

                options = []
                if len(display_rules.criterion.values) > 1:
                    if display_rules.criterion.input_type.render_type == 'select':
                        criterion_dict.update({'placeholder': 'Select'})
                        chvalues = [x for x in display_rules.criterion.values]
                        for chvalue in chvalues:
                            o = {'value': chvalue.value.id}
                            # o.update({'label':chvalue.value.code})
                            o.update({'label':chvalue.value.description})
                            options.append(o)
                    if display_rules.criterion.input_type.render_type == 'radio':
                        chvalues = [x for x in display_rules.criterion.values]
                        for chvalue in chvalues:
                            o = {'value': chvalue.value.id}
                            o.update({'label': chvalue.value.value_string})
                            o.update({'description': ""})
                            options.append(o)



                if len(options) > 0:
                    options = sorted(options, key=lambda d: d['value'])
                    # move unknown or not sure to end of the option list
                    for o in options:
                        if o['label'].upper() in ['UNKNOWN','NOT SURE']:
                            options.append(options.pop(options.index(o)))

                    criterion_dict.update({'options': options})

                # Get paths from triggered bys
                pathlist = []
                critlookup = {}
                path_tree = None
                for tb in display_rules.triggered_bys:
                    if tb.active:
                        tb_value = ''
                        if (tb.path):
                            pathlist.append(tb.path)
                        if tb.value.type == 'Integer':
                            try:
                                tb_value = int(tb.value.value_string)
                            except ValueError:
                                logger.error(f"Value {tb.value.value_string} cannot be converted to Integer") 
                        elif tb.value.type == 'Float':
                            try:
                                tb_value = float(tb.value.value_string)
                            except ValueError:
                                logger.error(f"Value {tb.value.value_string} cannot be converted to Integer") 
                        else:
                            tb_value = tb.value.id

                        critdict = {
                            "id": tb.criterion.id,
                            "value": tb_value,
                            "operator": tb.value.operator
                        }
                        critlookup[tb.id] = critdict

                # build tree
                # Q U E S T I O N : if len(pathlist) == 1?
                # if(pathlist):
                if display_rules.criterion.id == 100:
                    print(f"FOR 100 pathlist length {len(pathlist)}")
                    print(f"FOR 100 critlookup length {len(critlookup)}")
                if len(pathlist) == 2 or len(critlookup) == 1 or len(critlookup) == 2: 
                    critlist = []
                    for crit_key in critlookup:
                        if critlookup[crit_key]:
                            if display_rules.criterion.id == 81:
                                print(f"FOR 81 pathlist length {len(pathlist)}")
                                print(f"FOR 81 critlookup length {len(critlookup)}")
                                print(f"FOR 81 APPENDING: {critlookup[crit_key]}")
                            critlist.append(critlookup[crit_key])

                    path_tree = {
                        "operator": "AND",
                        "criteria": critlist 
                    }
                    # path_tree = update_dict(path_tree, critlookup)
                    if display_rules.criterion.id == 81:
                        print(f"FIRST PATH TREE FOR 81: {path_tree}")


                        # DO JUST 'AND' path_tree =

                    # if len(pathlist) == 1: # this shouldn't happen, but if it did...
                        # DO SOMETHING path_tree =
                        # ERROR???
                elif (pathlist):
                    path_tree = mc.get_tree(pathlist, suppress_header=True)
                    if display_rules.criterion.id == 100:
                        print(f"DR ID: {display_rules.id}")
                        print(f"DR CRITERION: {display_rules.criterion.id}")
                        print(f"SECOND PATH TREE FOR 100: {path_tree}")

                    path_tree = update_dict(path_tree, critlookup)

                    print(f"PATH TREE STRING: {path_tree}")
                # if no path list and length of critlookup is 1
                """
                elif len(critlookup) == 1:
                    path_tree = {
                        "operator": "AND",
                        "criteria": [
                            critlookup[tb.id]
                        ]
                    }
                    path_tree = update_dict(path_tree, critlookup)
                """

                if path_tree:
                    print(f"DR CRITERION: {display_rules.criterion.id}")
                    print(f"HERE IS THE PATH TREE: {path_tree}")
                    criterion_dict.update({'showIf':path_tree})
                # elif len(critlookup) == 1:
                #    criterion_dict.update({'showIf': critlookup[tb.id]})


                if display_rules.criterion.id == 81:
                    print(f"CRITERION DICT FOR 81: {criterion_dict}")
                if display_rules.criterion.id == 16:
                    print(f"CRITERION DICT FOR 16: {criterion_dict}")
            print(f"APPENDING: {criterion_dict}")
            F.append(criterion_dict)

        body = {"groups": json.dumps(G), "fields": json.dumps(F)}
        # body = {"groups": json.dumps(G), "fields": json.dumps(F)}
        body = {"groups": G, "fields": F}
        response = {
            "current_date": date.today().strftime("%B %d, %Y"),
            "current_time": strftime("%H:%M:%S +0000", gmtime()),
            "status": "OK",
            # "body": json.dumps(body)
            "body": body
        }
    return JSONResponse(response, HTTP_200_OK)


def init_app(app):
    app.include_router(mod, tags=["match_form"])