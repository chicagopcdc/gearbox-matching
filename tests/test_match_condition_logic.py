import pytest
import json
from sympy.core.sympify import sympify
from sympy.utilities.iterables import cartes

def get_expression(crit):
	temp_crit_with_op = []

	for i in range(len(crit)):
		if type(crit[i]) == dict:
			op = crit[i]['operator']
			if op == 'AND':
				op = '&'
			elif op == 'OR':
				op = '|'

			work_crit = crit[i]['criteria']

			for j in range(len(work_crit)):

				temp_crit_with_op.append(work_crit[j])

				if j != len(work_crit) -1:

					temp_crit_with_op.append(f" {op} ")

			temp_crit_with_op.append(")")
			temp_crit_with_op.insert(0,"(")

			return get_expression(crit[:i] +  temp_crit_with_op + crit[i+1:])
		
	return crit

def get_truth_table(expr_string):

    t_values = []
    tt = []
    print("IN get_truth_table 1")
    expr = sympify(expr_string)
    print("IN get_truth_table 2")
    variables = expr.free_symbols
    print("IN get_truth_table 3")

    for truth_values in cartes([False, True], repeat=len(variables)):
        values = dict(zip(variables, truth_values))
        if str(expr.subs(values)) == 'True':
            t_values.append(values)

        print("IN get_truth_table 4")

    for i in t_values:
        truth_vals = []
        for key, value in i.items():
            if value == True:
                truth_vals.append(int(str(key)[1:]))

        tt.append(sorted(truth_vals))

    return tt

# with open('data/match_conditions_compare_dat.json','r') as c:
#	conds_json = json.load(c)
# @pytest.mark.asyncio
def test_match_condition_logic(setup_database, client):
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/match-conditions", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    # full_res_str = '\n'.join([str(item) for item in full_res])

    # conds_json = json.load(get_match_conditions(setup_database, client))
    conds = full_res['body'][0]['algorithm']
    exp = get_expression([conds])

    # prepend the criteria id with 'x' b/c sympy needs alphanumeric 
    # to construct truth tables from a boolean exp
    print("boolean logic for study: ")
    print(''.join(f"{i}" for i in exp))
    exp_str = ''.join(f"{(i, 'x' + i)[i.isnumeric() == True]}" for i in exp)

    tt = get_truth_table(exp_str)

    # T O D O : FILTER OUT ANY EXTRA CRITERIA IN THE CRITERION SET WE ARE TESTING AGAINST,
    # THEN SORT THAT LIST
    assert not [1,2] in tt, "Criteria [1,2] does not meet the requirements for study 1."
