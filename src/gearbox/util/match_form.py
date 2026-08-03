from .bounds import bounds
from gearbox.routers import logger
from gearboxdatamodel.crud.match_form import get_form_info
from .match_conditions import get_tree


def update_dict(d, critlookup):
    for key in d:
        if key == "criteria":
            if isinstance(d[key], list):
                for i in range(0, len(d[key])):
                    if not isinstance(d[key][i], dict):
                        try:
                            d[key][i] = critlookup[int(d[key][i])]
                        except KeyError:
                            logger.error(
                                "Error message about improperly configured path - path ids do not exist for this..."
                            )

                    else:
                        update_dict(d[key][i], critlookup)
    return d


async def get_match_form(session):

    form_info = await get_form_info(session)

    G = []
    F = []

    for display_rules in form_info:
        criterion_dict = {}
        for ctag in display_rules.criterion.tags:
            g = {"id": ctag.tag.id, "name": ctag.tag.code}
            G.append(g)
            # get unique groups
            G = list({v["id"]: v for v in G}.values())
            G = sorted(G, key=lambda i: i["id"])

        if display_rules.active:
            criterion_dict = {"id": display_rules.criterion_id}
            for ctag in display_rules.criterion.tags:
                if ctag.tag.type == "form":
                    criterion_dict.update({"groupId": ctag.tag.id})
            if display_rules.criterion.active:
                code = display_rules.criterion.code
                criterion_dict.update({"name": code})
                if code in bounds.keys():
                    criterion_dict.update(bounds[code])

                criterion_dict.update({"label": display_rules.criterion.description})
                criterion_dict.update(
                    {"type": display_rules.criterion.input_type.render_type}
                )

                if display_rules.criterion.input_type.data_type.upper() == "INTEGER":
                    criterion_dict.update({"min": 0})
                if display_rules.criterion.input_type.data_type.upper() == "FLOAT":
                    criterion_dict.update({"min": 0})
                    criterion_dict.update({"step": 0.1})
                if display_rules.criterion.input_type.data_type.upper() == "PERCENTAGE":
                    criterion_dict.update({"min": 0})
                    criterion_dict.update({"max": 100})
                    criterion_dict.update({"step": 0.1})

                options = []
                if len(display_rules.criterion.values) > 1:
                    if display_rules.criterion.input_type.render_type == "select":
                        criterion_dict.update({"placeholder": "Select"})
                        chvalues = [x for x in display_rules.criterion.values]
                        for chvalue in chvalues:
                            o = {"value": chvalue.value.id}
                            # o.update({'label':chvalue.value.code})
                            o.update({"label": chvalue.value.description})
                            options.append(o)
                    if display_rules.criterion.input_type.render_type == "radio":
                        chvalues = [x for x in display_rules.criterion.values]
                        for chvalue in chvalues:
                            o = {"value": chvalue.value.id}
                            o.update({"label": chvalue.value.value_string})
                            o.update({"description": ""})
                            options.append(o)

                if len(options) > 0:
                    options = sorted(options, key=lambda d: d["value"])
                    # move unknown or not sure to end of the option list
                    for o in options:
                        if o["label"].upper() in ["UNKNOWN", "NOT SURE"]:
                            options.append(options.pop(options.index(o)))

                    criterion_dict.update({"options": options})

                # Get paths from triggered bys
                pathlist = []
                critlookup = {}
                path_tree = None
                for tb in display_rules.triggered_bys:
                    if tb.active:
                        tb_value = ""
                        if tb.path:
                            pathlist.append(tb.path)
                        if tb.value.type == "Integer":
                            try:
                                tb_value = int(tb.value.value_string)
                            except ValueError:
                                logger.error(
                                    f"Value {tb.value.value_string} cannot be converted to Integer"
                                )
                        elif tb.value.type == "Float":
                            try:
                                tb_value = float(tb.value.value_string)
                            except ValueError:
                                logger.error(
                                    f"Value {tb.value.value_string} cannot be converted to Integer"
                                )
                        else:
                            tb_value = tb.value.id

                        critdict = {
                            "id": tb.criterion.id,
                            "value": tb_value,
                            "operator": tb.value.operator,
                        }
                        critlookup[tb.id] = critdict

                # build tree
                if len(pathlist) == 2 or len(critlookup) == 1 or len(critlookup) == 2:
                    critlist = []
                    for crit_key in critlookup:
                        if critlookup[crit_key]:
                            critlist.append(critlookup[crit_key])

                    path_tree = {"operator": "AND", "criteria": critlist}
                    # if len(pathlist) == 1: # this shouldn't happen, but if it did...
                elif pathlist:
                    path_tree = get_tree(pathlist, suppress_header=True)
                    path_tree = update_dict(path_tree, critlookup)

                if path_tree:
                    criterion_dict.update({"showIf": path_tree})

            F.append(criterion_dict)

        match_form = {"groups": G, "fields": F}

    return match_form
