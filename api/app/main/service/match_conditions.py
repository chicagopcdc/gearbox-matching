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
