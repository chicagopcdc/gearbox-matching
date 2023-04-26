import json
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from gearbox.util import status
import re
from collections import deque
from gearbox.routers import logger
from gearbox.crud import study_algorithm_engine_crud, match_conditions
from gearbox.schemas import AlgorithmResponse
from sqlalchemy.ext.asyncio import AsyncSession as Session
from . import study_algorithm_engine

def expand_paths(paths):
    """
    this function expands the paths so that each criteria has it's own path

    :param paths: list of . separated criteria paths
    :return: list of expanded paths
    """
    expanded_paths = []
    for p in paths:
        build_p = ''
        for x in p.split('.'):
            build_p += x + '.'
            path = build_p.rstrip('.')
            if path not in expanded_paths:
                expanded_paths.append(path)
    return expanded_paths

 
def add_generation(pathlist):
    """
    the purpose of this function is to add a generation number
    to each node for each unique node / path combination
    it is necessary because depth first search requires nodes to be unique

    :param pathlist:
    :return: list of full paths with generation numbers for each node
    """

    result = []
    seen = {}
    nodelist = []

    for path in pathlist:
        if len(path.split('.')) > 1:
            # separate last node from the root
            m = re.search(r'^(.*)\.(.*)$', path)
            crit = m.group(2)
            root = m.group(1)

            if crit in seen:
                # if criteria with same root exists get current generation
                if root in seen[crit]:
                    gen = seen[crit][root]
                else:
                    # find the max generation for the crit to apply to crit / root
                    gen_max = max(seen[crit], key=seen[crit].get)
                    gen = seen[crit][gen_max] + 1
                    seen[crit][root] = gen
            # if this is a NEW criteria, add to seen
            else:
                seen[crit] = { root : 1 }
                gen = 1
        else:
            seen[path] = { '':[], 'gen':1 }
            result.append(path + '#' + '1')
            nodelist.append((path, path + '#' + '1'))

    # lookup and build path with generation for each node in path
    for path in pathlist:
        path_spl = path.split('.')
        pathstr = ''
        for crit in path_spl:
            crit_idx = path_spl.index(crit)
            rootstr = '.'.join(path_spl[:crit_idx])
            crit_gen = seen[crit][rootstr]
            if isinstance(seen[crit][rootstr],list):
                crit_gen = str(crit) + '#' + '1'
            else:
                crit_gen = str(crit) + '#' + str(seen[crit][rootstr])
            pathstr += crit_gen + '.'

        result.append(pathstr.rstrip('.'))
    return result

# create and return graph from full paths
def merged(full_paths, X={}):
    """
    this function builds a graph from a list of paths
    :param full_paths: 

    :return: graph of criteria
    """
    for path in full_paths:
        node = X
        for p in path.split('.'):
            node = node.setdefault(p, dict())
    return X

def get_new_node(crit, op=""):
    if isinstance(crit, list):
        return { "operator": op, "criteria": crit }
    else:
        return { "operator": op, "criteria": [crit] }

def get_nodes_and_children(visited, children_dict, X, node):
    """
    this function builds a dict of all nodes and immediate children

    :return: dict of nodes and immediate children
    """
    if node not in visited:
        visited.add(node)
        children_dict.update({node: list(X[node].keys())})
        for child in X[node].keys():
            get_nodes_and_children(set(), children_dict, X[node], child)
        return children_dict

def dfs(visited, node_list, graph, node):
    """
    this function builds a list of node / neighbor tuples
    and removes generation number

    :return: list of node / neighbor tuples
    """
    if node not in visited:
        visited.add(node)
        for neighbor in graph[node]:
            node_list.append((node, neighbor))
            dfs(visited, node_list, graph, neighbor)
        # strip out generation information and return node list
        return [ (x[0].split('#')[0], x[1].split('#')[0])  for x in node_list ]

def build_tree(nodelist):
    """
    this function builds json which represents criteria
    for a trial study. the function iterates through
    the list of node / neighbor pairs and uses a stack
    to build the nodes. nodes that contain explicit operators
    are in the dash separated format: 
    node#-explicit_operator-group-id

    where group-id is used to define the scope
    of the explicit operator

    when not explicitly defined, operators are assumed
    to be 'AND' when criteria are indicated sequentially
    and 'OR' for criteria at the same level (branch)

    :param nodelist: list of node / neighbor pairs

    :return: json criteria
    """

    crit_que = deque()

    groups_seen = set()

    for i in range(len(nodelist)):

        node, neighbor = nodelist[i]

        group_id = ''
        node_operator = ''
        neighbor_group_id = ''
        neighbor_operator = ''
        check_ahead_node = ''
        check_ahead_group_id = ''
        check_ahead_node_operator = ''

        # if there is an explicit operator in the 
        # node or neighbor extract it 
        m = re.search(r'^(.*)-(.*)-(.*)$', node)
        if m:
            node = int(m.group(1))
            node_operator = m.group(2)
            group_id = m.group(3)
            groups_seen.add(group_id)
        else:
            node = int(node)

        m = re.search(r'^(.*)-(.*)-(.*)$', neighbor)
        if m:
            neighbor = int(m.group(1))
            neighbor_operator = m.group(2)
            neighbor_group_id = m.group(3)
        else:
            neighbor = int(neighbor)

        # peek at next node - used to establish
        # the existence of a child node
        if i < len(nodelist) - 1:
            check_ahead_node = nodelist[i+1][0]
            m = re.search(r'^(.*)-(.*)-(.*)$', check_ahead_node)
            if m:
                check_ahead_node = int(m.group(1))
                check_ahead_node_operator = m.group(2)
                check_ahead_group_id = m.group(3)
            else:
                check_ahead_node = int(check_ahead_node)

        # start to build the tree
        if len(crit_que) == 0:

            root_node = get_new_node(node, 'AND')
            crit_que.append(root_node)

            if neighbor_operator:
                if neighbor_operator == 'AND':
                    root_node['criteria'].append(neighbor)
                    crit_que.append((root_node, neighbor_group_id))
                else:
                    n_node = get_new_node(neighbor, neighbor_operator)
                    root_node['criteria'].append(n_node)
                    crit_que.append((root_node, neighbor_group_id))
                    crit_que.append((n_node, neighbor_group_id))
            elif check_ahead_node == neighbor:
                n_node = get_new_node(neighbor, 'AND')
                root_node['criteria'].append(n_node)
                crit_que.append(n_node)
            else:
                n_node = get_new_node(neighbor, 'OR')
                root_node['criteria'].append(n_node)
                crit_que.append(n_node)

        else:

            ####################################################
            #   POP FROM THE QUE TO GET WORKING NODE
            ####################################################
            working_node = crit_que.pop()
            working_group_id = ''

            #######################################################
            #  GET GROUP ID IF WORKING NODE IS PART OF A GROUP
            #  IF working_node IS PART OF A GROUP IT IS PUSHED
            #  TO THE STACK AS A TUPLE
            #######################################################
            if type(working_node) is tuple:
                working_node, working_group_id = working_node

            ################################################################
            #  MAIN CASE 1: NODE IS A DIRECT CHILD OF THE WORKING NODE
            ################################################################
            if working_node['criteria'][-1] == node and (neighbor_group_id == working_group_id or neighbor_group_id == ''):
                
                ################################################################
                # IF THERE IS NO EXPLICIT OPERATOR
                ################################################################
                if not neighbor_operator:

                    ################################################################
                    # IF THERE IS NOT ALREADY AN 'AND' ON THE NODE THEN ADD
                    # 'AND' AND NEIGHBOR CRITERIA
                    ################################################################
                    if working_node['operator'] != 'AND':
                        n_node = get_new_node(working_node['criteria'][0],'AND')
                        n_node['criteria'].append(neighbor)
                        working_node['criteria'][-1] = n_node
                        if working_group_id:
                            crit_que.append((working_node, working_group_id))
                            crit_que.append((n_node, working_group_id))
                        else:
                            crit_que.append(working_node)
                            crit_que.append(n_node)
                    ################################################################
                    # IF THERE IS AN 'AND' ON THE NODE THEN JUST APPEND
                    # NEIGHBOR CRITERIA
                    ################################################################
                    else:
                        working_node['criteria'].append(neighbor)
                        if working_group_id:
                            crit_que.append((working_node, working_group_id))
                        else:
                            crit_que.append(working_node)

                #####################################################################
                # DIRECT CHILD HAS EXPLICIT OPERATOR
                #####################################################################
                else:
                    working_node['criteria'].append(neighbor)
                    crit_que.append((working_node, working_group_id))

            ################################################################
            # MAIN CASE 2: NODE IS NOT A DIRECT CHILD OF THE WORKING NODE
            #   NODE IS PART OF THE SAME GROUP AS THE WORKING NODE
            ################################################################
            elif neighbor_group_id == working_group_id and neighbor_group_id:

                ########################################################
                # IF NODE IS IN THE CRITERIA LIST OF THE WORKING NODE THEN
                # JUST APPEND NEIGHBOR
                ########################################################
                if node in working_node['criteria']:
                    working_node['criteria'].append(neighbor)
                    crit_que.append(working_node)

                elif working_node['operator'] == 'OR':

                    ########################################################
                    # IF NEIGHBOR DOESN'T HAVE CHILDREN JUST APPEND
                    # AND PUSH
                    ########################################################
                    if neighbor != check_ahead_node and working_node:
                        working_node['criteria'].append(neighbor)
                        crit_que.append((working_node,working_group_id))

                    ########################################################
                    # IF NEIGHBOR HAS CHILDREN CREATE THE 'AND'
                    ########################################################
                    else: 
                        n_node = get_new_node(neighbor, 'AND')
                        working_node['criteria'].append(n_node)
                        crit_que.append(working_node)
                        crit_que.append(n_node)

                #################################################################################
                # POP UNTIL WE FIND THE PARENT WITH THE SAME OPERATOR 
                #################################################################################
                else:
                    while working_node['operator'] != neighbor_operator and neighbor_operator:
                        try:
                            working_node = crit_que.pop()
                            if type(working_node) is tuple:
                                working_group_id = working_node[1]
                                working_node = working_node[0]
                        except:
                            # print("no more nodes")
                            break

                    ########################################################
                    # IF NEIGHBOR HAS CHILDREN CREATE THE "AND" AND APPEND
                    ########################################################
                    if neighbor == check_ahead_node:
                        c_node = get_new_node(neighbor,'AND')
                        working_node['criteria'].append(c_node)
                        crit_que.append((working_node, neighbor_group_id))
                        crit_que.append((c_node, neighbor_group_id))

                    ########################################################
                    # IF NEIGHBOR HAS NO CHILDREN JUST APPEND
                    ########################################################
                    else:
                        working_node['criteria'].append(neighbor)
                        crit_que.append((working_node, neighbor_group_id))

            ################################################################
            # MAIN CASE 3: NODE IS NOT A DIRECT CHILD OF THE WORKING NODE,
            # NODE IS NOT PART OF THE SAME GROUP AS THE WORKING NODE
            ################################################################
            else:
                ######################################################################
                # FIND MOST RECENT GROUP NODE IF NEIGHBOR GROUP ID HAS ALREADY
                # BEEN SEEN
                ######################################################################
                if neighbor_group_id in groups_seen:
                    while neighbor_group_id != working_group_id:
                        try:
                            working_node = crit_que.pop()
                            if type(working_node) is tuple:
                                working_group_id = working_node[1]
                                working_node = working_node[0]
                        except:
                            # print("no more nodes")
                            break

                ######################################################################
                # FIND PARENT NODE
                ######################################################################
                else:
                    while node not in working_node['criteria']:
                        try:
                            working_node = crit_que.pop()
                            if type(working_node) is tuple:
                                working_group_id = working_node[1]
                                working_node = working_node[0]
                        except:
                            # print("no more nodes")
                            break

                #################################################################
                # IF NEIGHBOR HAS CHILDREN
                #################################################################
                if neighbor == check_ahead_node:

                    #################################################################
                    # IF NEIGHBOR HAS AN EXPLICIT OPERATOR
                    #################################################################
                    if neighbor_operator:

                        #################################################################
                        # IF NEIGHBOR IS PART OF THE SAME GROUP AS WORKING NODE
                        # THEN CREATE "AND" FOR CHILDREN AND APPEND
                        #################################################################
                        if neighbor_group_id == working_group_id:
                            c_node = get_new_node(neighbor,'AND')
                            working_node['criteria'].append(c_node)
                            crit_que.append((working_node, neighbor_group_id))
                            crit_que.append((c_node, neighbor_group_id))
                        else:
                            ###################################################################
                            # NEIGHBOR (HAS CHILDREN) IS PART OF A DIFFERENT GROUP SO CREATE
                            # GROUP NODE 
                            ###################################################################
                            n_node = get_new_node(neighbor, neighbor_operator)
                            working_node['criteria'].append(n_node)
                            crit_que.append((working_node, neighbor_group_id))
                            crit_que.append((n_node, neighbor_group_id))

                    ###################################################################
                    # IF THE WORKING NODE ALREADY HAS AN OPERATOR (AND THE
                    # NEIGHBOR HAS AN OPERATOR)
                    ###################################################################
                    elif isinstance(working_node['criteria'][1], dict): 

                        if working_node['criteria'][1]['operator'] == 'OR':
                            n_node = get_new_node(neighbor, 'AND')
                            working_node['criteria'][1]['criteria'].append(n_node)
                            crit_que.append(working_node)
                            crit_que.append(n_node)

                        ###################################################################
                        # SPLIT AT THE BRANCH AND ADD THE 'OR"
                        ###################################################################
                        else:
                            node_idx = working_node['criteria'].index(node)
                            working_node_crit = working_node['criteria'][node_idx+1:]
                            working_node['criteria'] = working_node['criteria'][:node_idx+1] 
                            wrapper_node = get_new_node(working_node_crit, 'OR')
                            working_node['criteria'].append(wrapper_node)
                            new_crit_node = get_new_node(neighbor, 'AND')
                            wrapper_node['criteria'].append(new_crit_node)
                            crit_que.append(working_node)
                            crit_que.append(wrapper_node)
                            crit_que.append(new_crit_node)

                    #########################################################################
                    # WORKING NODE CRITERIA IS A LIST AND DOES NOT ALREADY HAVE
                    # AN 'OR' SO SPLIT AT THE BRANCH AND ADD 'OR'
                    #########################################################################
                    else:
                        node_idx = working_node['criteria'].index(node)
                        working_node_crit = working_node['criteria'][node_idx+1:]
                        working_node['criteria'] = working_node['criteria'][:node_idx+1:] 
                        existing_crit_node = get_new_node(working_node_crit, 'AND')
                        wrapper_node = get_new_node(existing_crit_node, 'OR')
                        working_node['criteria'].append(wrapper_node)
                        new_crit_node = get_new_node(neighbor, 'AND')
                        wrapper_node['criteria'].append(new_crit_node)
                        crit_que.append(working_node)
                        crit_que.append(wrapper_node)
                        crit_que.append(new_crit_node)

                #################################################################
                # NEIGHBOR HAS NO CHILDREN, SO JUST ADD
                #################################################################
                else:
                    if neighbor_operator:

                            ############################################################
                            # IF THE OPERATOR IS THE SAME AS THE WORKING NODE
                            # THEN JUST APPEND THE NEIGHBOR
                            ############################################################
                            if neighbor_operator == working_node['operator']:
                                working_node['criteria'].append(neighbor)
                                crit_que.append((working_node, neighbor_group_id))

                            ############################################################
                            # IF THE OPERATOR IS NOT THE SAME AS THE WORKING NODE
                            # THEN CREATE A NODE FOR IT AND THEN APPEND TO THE
                            # WORKING NODE
                            ############################################################
                            else:
                                n_node = get_new_node(neighbor, neighbor_operator)
                                working_node['criteria'].append(n_node)
                                crit_que.append((working_node, neighbor_group_id))
                                crit_que.append((n_node, neighbor_group_id))

                    ###################################################################
                    # THIS elif NEEDS TEST DATA
                    ###################################################################
                    elif isinstance(working_node['criteria'][1], dict): 
                        if working_node['criteria'][1]['operator'] == 'OR':
                            working_node['criteria'][1]['criteria'].append(neighbor)
                            crit_que.append(working_node)
                        else:
                            node_idx = working_node['criteria'].index(node)
                            working_node_crit = working_node['criteria'][node_idx+1:]
                            working_node['criteria'] = working_node['criteria'][:node_idx+1:]
                            wrapper_node = get_new_node(working_node_crit, 'OR')
                            working_node['criteria'].append(wrapper_node)
                            wrapper_node['criteria'].append(neighbor)
                            crit_que.append(working_node)
                            crit_que.append(wrapper_node)
                    else:
                            ############################################################
                            # SPLIT NODE AND CREATE 'OR'
                            ############################################################
                            node_idx = working_node['criteria'].index(node)
                            working_node_crit = working_node['criteria'][node_idx+1:]
                            working_node['criteria'] = working_node['criteria'][:node_idx+1]
                            wrapper_node = get_new_node(working_node_crit, 'OR')
                            working_node['criteria'].append(wrapper_node)
                            wrapper_node['criteria'].append(neighbor)
                            crit_que.append(working_node)
                            crit_que.append(wrapper_node)

    # return the first node
    return crit_que[0]

def get_tree(full_paths, study_id=None, suppress_header=False):
    fp = expand_paths(full_paths)
    fpg = add_generation(fp)
    mgd = merged(fpg)
    dfd = get_nodes_and_children(set(), {}, mgd, fpg[0])

    node_list = dfs(set(), [], dfd, fpg[0])
    criteria_tree = build_tree(node_list)

    if isinstance(criteria_tree, tuple):
        criteria_tree = criteria_tree[0]

    if (suppress_header):
        return_criteria = criteria_tree
    else:
        return_criteria = { "studyId" : study_id,
            "algorithm": criteria_tree }


    return return_criteria

async def get_match_conditions(session: Session) -> List[AlgorithmResponse]:

    active_match_conds = await match_conditions.get_study_algorithm_engines(session=session)
    match_conds = []

    for a in active_match_conds:
        study_logic = {}
        study_logic['studyId'] = a.study_version.study_id
        study_logic['algorithm'] = a.study_algorithm_engine.algorithm_logic
        match_conds.append(study_logic)

    # check for duplicate study ids in match conditions list, this can happen if
    # there are more than 1 active entry for a study in the eligibility_criteria_info table
    studyIds = [ x['studyId'] for x in match_conds ]
    dupes = [ x for n, x in enumerate(studyIds) if x in studyIds[:n]]
    if dupes:
        logger.error(f"Duplicte active studies found in eligibility_criteria_info table for the following study ids: {dupes}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 
            f"Duplicte active studies found in eligibility_criteria_info table for the following study ids: {dupes}") 

    # sort by studyId before returning
    match_conds = sorted(match_conds, key=lambda k: k['studyId'])

    return match_conds