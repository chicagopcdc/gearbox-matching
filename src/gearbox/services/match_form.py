from gearbox import config
import json
from ..util.bounds import bounds
from . import logger
from gearbox.crud.match_form import get_form_info, clear_dr_tb_tags, insert_display_rules, insert_triggered_by, insert_tags
from .match_conditions import get_tree
from gearbox.schemas import MatchForm 
from gearbox.services import value as value_service
from fastapi import HTTPException, Request
from gearbox.util import status, bucket_utils
from sqlalchemy.ext.asyncio import AsyncSession as Session
from gearbox.services import unit as unit_service
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession as Session
from gearbox.util import status

import re

async def build_match_form(session: Session, request: Request, save: bool):

    match_form = await get_match_form(session)
    if save:
        if not config.BYPASS_S3:
            params = [{'Content-Type':'application/json'}]
            bucket_utils.put_object(request, config.S3_BUCKET_NAME, config.S3_BUCKET_MATCH_FORM_KEY_NAME, config.S3_PUT_OBJECT_EXPIRES, params, match_form)

    return match_form

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

async def get_match_form(session:Session)-> MatchForm:

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
                if ctag.tag.type == 'form':
                    criterion_dict.update({'groupId': ctag.tag.id})
            if display_rules.criterion.active:
                code = display_rules.criterion.code
                criterion_dict.update({'name': code})
                if code in bounds.keys():
                    criterion_dict.update(bounds[code])

                criterion_dict.update({'label':display_rules.criterion.description})
                criterion_dict.update({'type':display_rules.criterion.input_type.render_type})

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
                triggered_bys = [x for x in display_rules.triggered_bys]
                for tb in triggered_bys:
                    if tb.active:
                        tb_value = ''
                        if (tb.path):
                            pathlist.append(tb.path)
                        # MODIFY TO tb.value.is_numeric
                        if tb.value.is_numeric:
                            try:
                                tb_value = float(tb.value.value_string)
                            except ValueError:
                                logger.error(f"Value {tb.value.value_string} cannot be converted to number") 
                        else:
                            tb_value = tb.value.id

                        critdict = {
                            "id": tb.criterion.id,
                            "value": tb_value,
                            "valueId": tb.value.id,
                            "operator": tb.value.operator
                        }
                        critlookup[tb.id] = critdict

                if len(pathlist) == 2 or len(critlookup) == 1 or len(critlookup) == 2:
                    critlist = []
                    for crit_key in critlookup:
                        if critlookup[crit_key]:
                            critlist.append(critlookup[crit_key])


                    m = re.search("OR", str(pathlist))
                    if m and len(pathlist) == 1:
                        path_tree = {
                            "operator": "OR",
                            "criteria": critlist 
                        }
                    else:
                        path_tree = {
                            "operator": "AND",
                            "criteria": critlist 
                        }

                elif (pathlist):
                    path_tree = get_tree(pathlist, suppress_header=True)
                    path_tree = update_dict(path_tree, critlookup)

                if path_tree:
                    criterion_dict.update({'showIf':path_tree})

            F.append(criterion_dict)

        match_form = {"groups": G, "fields": F}

    return match_form

async def update(match_form:MatchForm, session:Session):
    priority = 0
    display_rules_id = 0
    triggered_by_id = 0
    dr_rows = []
    tb_rows = []
    tag_rows = []
    for field in match_form.fields:
        dr_row = {}
        tb_row = {}
        tag_row = {}

        tag_row['criterion_id'] = field.id
        tag_row['tag_id'] = field.groupId
        tag_rows.append(tag_row)

        priority += 1000
        display_rules_id += 1
        display_rules_criterion_id = field.id
        dr_row['id'] = display_rules_id
        dr_row['criterion_id'] = display_rules_criterion_id
        dr_row['priority'] = priority
        dr_row['active'] = 1
        dr_row['version'] = 1
        dr_rows.append(dr_row)
        if field.showIf:
            show_if_criteria = field.showIf.get('criteria')
            path_ids = []
            show_if_path_count = 0
            for show_if_criterion in show_if_criteria:
                show_if_path_count += 1
                triggered_by_id += 1
                path_ids.append(triggered_by_id)
                tb_row['id'] = triggered_by_id
                tb_row['display_rules_id'] = display_rules_id   
                tb_row['criterion_id'] = show_if_criterion.get('id')
                value_id = show_if_criterion.get('valueId')

                if value_id:
                    tb_row['value_id'] = value_id
                else:
                    operator = show_if_criterion.get('operator')
                    value = show_if_criterion.get('value')
                    unit_name = show_if_criterion.get('unit')
                    if not unit_name:
                        unit_name = 'none'
                    is_numeric = show_if_criterion.get('is_numeric')

                    if is_numeric:
                        try:
                            check_value_num = float(value)
                        except ValueError:
                            logger.error(f"Value {value} cannot be converted to number") 
                            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                f"Value {value} cannot be converted to number")
                    # get value_id from existing or new value
                    value_id = await value_service.get_value_id(
                        session=session,
                        value_str=value, 
                        operator=operator,
                        unit=unit_name,
                        is_numeric=is_numeric
                        )
                    tb_row['value_id'] = value_id

                tb_row['active'] = True
                if show_if_path_count > 1:
                    tb_row['path'] ='.'.join(map(str,path_ids))
                tb_rows.append(tb_row)
                tb_row = {}
    await clear_dr_tb_tags(current_session=session) 
    await insert_tags(current_session=session, tag_rows=tag_rows)
    await insert_display_rules(current_session=session, display_rules_rows=dr_rows)
    await insert_triggered_by(current_session=session, triggered_by_rows=tb_rows)
