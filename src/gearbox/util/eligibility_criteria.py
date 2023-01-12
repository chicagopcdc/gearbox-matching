from gearbox.crud.eligibility_criteria import get_eligibility_criteria_info

async def get_eligibility_criteria(session):

    results = await get_eligibility_criteria_info(session)
    eligibility_criteria = []

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
                eligibility_criteria.append(f)
    else:
        eligibility_criteria = []
    

    return eligibility_criteria