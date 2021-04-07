from operator import getitem
from functools import reduce
import json
import copy

import logging

##################################

def get_full_paths(pps, ops):
    full_paths = []
    for i in range(1, len(pps)): #start with index 1, ignore first root
        if ops[i] and not ops[i]=='AND': #its OR
            full_paths.append(pps[i-1])
    return full_paths

def merged(full_paths, X={}):
    #full_paths list to merged nested dicts
    for path in full_paths:
        node = X
        for p in path.split('.'):
            node = node.setdefault(p, dict())
    return X

def get_from_dict(X, keys):
    return reduce(getitem, keys, X)

def set_nested_item(dataDict, mapList, val):
    reduce(getitem, mapList[:-1], dataDict)[mapList[-1]] = val
    return dataDict

def get_path(data, target, trunk=[]):
    if isinstance(data, dict):
        for key, val in data.items():
            t = trunk + [key,]
            if val == target: 
                yield t
            else:
                yield from get_path(val, target, t)
    elif isinstance(data, list):
        for item in data:
            idx = data.index(item)
            t = trunk + [idx,]
            val = data[idx]
            if val == target:
                yield t
            else:
                yield from get_path(val, target, t)

def dfs(visited, children_list, X, node):
    if node not in visited:
        visited.add(node)
        children_list.append({node: list(X[node].keys())})
        for child in X[node].keys():
            dfs(set(), children_list, X[node], child)
        return children_list

def replace(data, match, repl):
    if isinstance(data, dict):
        if data == match:
            return repl
        else:
            return {k: replace(v, match, repl) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace(i, match, repl) for i in data]
    else:
        return repl if data == match else data

def repeats_to_dollars(M, y, p):
    matches = []
    q = 0
    for path in y[:-1]:
        match = get_from_dict(M, path[:-2])
        matches.append(match)
        set_nested_item(M, path[:-2], "$$$"+str(q))
        q+=1
    return M, matches

def dollars_to_repeats(M, y, matches):
    q=0
    for match in matches:
        set_nested_item(M, y[q][:-2], match)
        q+=1
    return M

def format(X):
    A=[]
    roots = list(X.keys())
    
    for root in roots:
        #get list of {parent:[children]} for parent nodes in depth first
        PC = dfs(set(), [], X, root)

        #set the first one to get the dict going
        pc = PC[0]
        c = list(pc.values())
        M = {'operator': 'AND', 'criteria': [root, {'operator': 'OR', 'criteria': c[0]}]}

        anded = 0 # needed for triggering C, which follows an A (anded) group
        i=1 #start at 1 since i did the 0th above
        while i < len(PC):

            pc=PC[i]
            p = list(pc.keys())
            c = list(pc.values())

            crits = [p[0]]
            p_match = p[0]

            if len(c[0])==1: #keep appending these until we hit the bud
                while len(c[0])==1:
                    crits.append(c[0][0])
                    i+=1
                    pc=PC[i]
                    p = list(pc.keys())
                    c = list(pc.values())

                if len(c[0])>1:
                    """case A - anding"""
                    anded=1

                    #swap out pre-set with $$$
                    y = [x for x in get_path(M, p_match)]
                    if len(y)>1:
                        M, matches = repeats_to_dollars(M, y, p_match)

                    #make the replacement of interest
                    repl = {'operator': 'AND', 'criteria': crits + ['****']}
                    m = replace(M, p_match, repl)
                    M = copy.deepcopy(m)

                    #restore the $$$
                    if len(y)>1:
                        M = dollars_to_repeats(M, y, matches)

                else:
                    """case  B - single bud, not anded"""
                    #swap out pre-set with $$$
                    y = [x for x in get_path(M, p_match)]
                    if len(y)>1:
                        M, matches = repeats_to_dollars(M, y, p_match)

                    #make the replacement of interest
                    repl = {'operator': 'AND', 'criteria': crits}
                    m = replace(M, p_match, repl)
                    M = copy.deepcopy(m)

                    #restore the $$$
                    if len(y)>1:
                        M = dollars_to_repeats(M, y, matches)

                    #i allows us to skip ahead to do anding
                    i+=1
            else:
                if anded:
                    """case C - post-anding"""
                    anded=0

                    #this case doe snot need dollars replacements               
                    repl = {'operator': 'OR', 'criteria': c[0]}
                    m = replace(M, '****', repl)
                    M = copy.deepcopy(m)

                elif c[0]==[]:
                    """case D - terminal-bud"""
                    #swap out pre-set with $$$
                    y = [x for x in get_path(M, p[0])]
                    if len(y)>1:
                        M, matches = repeats_to_dollars(M, y, p[0])

                    repl = {'operator': 'AND', 'criteria': [p[0]]}
                    m = replace(M, p[0], repl)
                    M = copy.deepcopy(m)

                    #restore the $$$
                    if len(y)>1:
                        M = dollars_to_repeats(M, y, matches)

                else:
                    """case E -- default: parent has multiple children"""
                    #swap out pre-set with $$$
                    y = [x for x in get_path(M, p[0])]
                    if len(y)>1:
                        M, matches = repeats_to_dollars(M, y, p[0])

                    repl = {'operator': 'AND', 'criteria': [p[0], {'operator': 'OR', 'criteria': c[0]}]}
                    m = replace(M, p[0], repl)
                    M = copy.deepcopy(m)

                    #restore the $$$
                    if len(y)>1:
                        M = dollars_to_repeats(M, y, matches)

                #i sets PC[i]
                i+=1

        A.append(M)

    R = []
    i = 0
    for a in A:
        r = {'studyId': i, 'algorithm': a}
        R.append(r)
        i+=1

    return R


def groups(tags):
    G = []
    for tag in tags:
        g = {
            'id': tag['id'],
            'name': tag['code']
        }
        G.append(g)
    return G


def exactly_1(row):
    if isinstance(row, dict):
        return True
    elif isinstance(row, list):
        if len(row)==1:
            return True
        else:
            return False
    else:
        return False


def is_active(row):
    if exactly_1(row):
        if row['active'] is None:
            return True #assume null = active
        else:
            return bool(row['active'])
    else:
        logging.warning("is_active() cannot operate on multiple rows\n")
        return False


def triggers(row, triggered_by, value):
    display_rules_id = row['id']
    tbs = list(filter(lambda x: x['display_rules_id'] == display_rules_id, triggered_by))
    
    if len(tbs)>0:
        for tb in tbs: #can be triggered by more than one crit/val combo
            if is_active(tb):
                criterion_id = tb['criterion_id']

                #get val and operator
                value_id = tb['value_id']
                val = list(filter(lambda x: x['id'] == value_id, value))[0]
                if exactly_1(val) and is_active(val):
                    operator = val['operator']
                    the_value = val['value_string']
                else:
                    return {}
                
                path = tb['path']
                #if not path is None:
                if path:
                    try:
                        crits = showIf.get('criteria')
                        new_crit = {
                            'id': criterion_id,
                            'operator': operator,
                            'value': eval(the_value)
                        }
                        crits.append(new_crit)
                        showIf.update({'criteria': crits})
                    except Exception as e:
                        logging.error(e)
                else: #if path, it comes in 2nd, 3rd, etc crit. set showIf for building upon)
                    showIf = {
                        'operator': 'OR', #always OR as scripted for now
                        'criteria': [
                            {
                                'id': criterion_id,
                                'operator': operator,
                                'value': eval(the_value)
                            }
                        ]
                    }
                    
        return showIf
    else:
        return {}

bounds = {
    'age': {'min': 0},
    'weight': {'min': 0},
    'refractoryEvents': {'min': 0},
    'chemoCycles': {'min': 0},
    'relapseEvents': {'min': 0},
    'blastPerc': {'min': 0, 'max': 100, 'step': 0.1},
    'blastPercMethod': {'min': 0},
    'Days since last dose of any cytotoxic agent (with exception of hydroxyurea)': {'min': 0},
    'Days since last dose of any cytotoxic agent (with exception of low-dose cytarabine)': {'min': 0},
    'Alanine transaminase (ALT), in IU/L': {'min': 0.1, 'step': 0.1},
    'Days since last dose of steroids': {'min': 0},
    'anthracycline dose': {'min': 0.1, 'step': 0.1},
    'Direct bilirubin (in mg/dL)': {'min': 0.1, 'step': 0.1},
}


def form(display_rules, input_type, criterion, criterion_has_tag, criterion_has_value, value, triggered_by):
    F = []

    sorted_display_rules = sorted(display_rules, key = lambda i: i['priority'])

    for row in sorted_display_rules: 
        #if row is not active, do nothing
        if is_active(row):
            criterion_id = row['criterion_id']

            #1 of the 4 required
            f = {'id': criterion_id}

            cht = list(filter(lambda x: x['criterion_id'] == criterion_id, criterion_has_tag))[0]
            tag_id = cht['tag_id']
            
            #2 of the 4 required
            f.update({'groupId': tag_id})

            crit = list(filter(lambda x: x['id'] == criterion_id, criterion))[0]
            
            if exactly_1(crit): #should always be true
                if is_active(crit):
                    #set the name
                    #3 of 4 required
                    the_name = crit['code']
                    f.update({'name': the_name})

                    #bounds
                    if the_name in bounds.keys():
                        for k, v in bounds[the_name].items():
                            f.update({k: v})

                    #set the label
                    f.update({'label': crit['display_name']})

                    #prep to set the type
                    input_type_id = crit['input_type_id']
                    it = list(filter(lambda x: x['id'] == input_type_id, input_type))[0]

                    #set the type
                    #4 of 4 required
                    f.update({'type': it['render_type']})

                    #convert any into showIf statement
                    showIf = triggers(row, triggered_by, value)
                    if showIf:
                        f.update({'showIf': showIf})

                    #see if muliple values
                    chv = list(filter(lambda x: x['criterion_id'] == criterion_id, criterion_has_value))
                    if len(chv) in [0, 1]:
                        pass
                    else: #criterion has multiple vals
                        if f.get('type') == 'select':
                            f.update({'placeholder': 'Select'})

                        options = []
                        vals = [x['value_id'] for x in chv]
                        for val in vals:
                            
                            o = {'value': val}

                            v_row = list(filter(lambda x: x['id'] == val, value))[0]
                            o.update({'label': v_row['code']})

                            #description not used anymore?
                            #o.update({'description': v_row['description']})
                            o.update({'description': ""})

                            options.append(o)

                        f.update({'options': options})
        F.append(f)

    return F
