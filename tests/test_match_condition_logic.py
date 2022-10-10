import pytest
import json
from sympy.core.sympify import sympify
from sympy.utilities.iterables import cartes

# T O D O:  create a test that compares truth table produced from API endpoint vs
# truth table from mock data

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
    expr = sympify(expr_string)
    variables = expr.free_symbols

    for truth_values in cartes([False, True], repeat=len(variables)):
        values = dict(zip(variables, truth_values))
        if str(expr.subs(values)) == 'True':
            t_values.append(values)

    for i in t_values:
        truth_vals = []
        for key, value in i.items():
            if value == True:
                truth_vals.append(int(str(key)[1:]))

        tt.append(sorted(truth_vals))

    return tt

@pytest.mark.asyncio
def test_match_condition_logic(setup_database, client):
    """
    This test pulls match-conditions from the backend, transforms the json into 
    a boolean expression, and then produces a table containing all possible criteria combinations
    that satisfy the boolean expression. It then tests 2 sets of criteria
    against this list, one complete and one incomplete. 
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/build-match-conditions", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    # conds = full_res['body'][0]['algorithm']
    conds = full_res[0]['algorithm']
    exp = get_expression([conds])
    exp = [str(x) for x in exp]

    # prepend the criteria id with 'x' b/c sympy needs alphanumeric 
    # to construct truth tables from a boolean exp
    exp_str = ''.join(f"{(i, 'x' + i)[i.isnumeric() == True]}" for i in exp)
    exp_univ = set([ i for i in exp if i.isnumeric() == True])

    tt = get_truth_table(exp_str)

    # TEST FAIL
    test_form_crits = [1,4,5,8,12,9] # FAIL STUDY 1
    test_form_crits_cleaned = sorted([i for i in test_form_crits if str(i) in exp_univ])
    print(f"Test form criteria: {test_form_crits_cleaned}")
    if test_form_crits_cleaned in tt:
        errors.append(f"Criteria {test_form_crits_cleaned} should not have met the requirements for study 1.")

    # TEST PASS
    test_form_crits = [1,2,13,8,99] # PASS STUDY 1
    test_form_crits_cleaned = sorted([i for i in test_form_crits if str(i) in exp_univ])
    print(f"Test form criteria: {test_form_crits_cleaned}")
    if not test_form_crits_cleaned in tt:
        errors.append(f"Criteria {test_form_crits_cleaned} should have met the requirements for study 1.")

    assert not errors, f"Errors occurred: {errors}"
