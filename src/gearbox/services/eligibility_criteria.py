from gearbox.crud import eligibility_criteria_crud
from gearbox.schemas import EligibilityCriteriaCreate, EligibilityCriteriaSearchResults, EligibilityCriteria as EligibilityCriteriaSchema
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import HTTPException
from gearbox.util import status

async def reset_active_status(session: Session, study_version_id: int) -> bool:
    # set all rows related to the study_version to false
    sae_to_update = await eligibility_criteria_crud.get_multi(
        db=session, 
        active=True, 
        where=[f"eligibility_criteria.study_version_id = {study_version_id}"]
    )
    for sae in sae_to_update:
        # set all to false
        await eligibility_criteria_crud.update(db=session, db_obj=sae, obj_in={"active":False})
    return True

async def get_eligibility_criteria(session: Session, id: int) -> EligibilityCriteriaSchema:
    ec = await eligibility_criteria_crud.get(session, id)
    return ec

async def get_eligibility_criteria(session: Session) -> EligibilityCriteriaSearchResults: 
    ecs = await eligibility_criteria_crud.get_multi(session)
    return ecs
    pass

async def create_eligibility_criteria(session: Session, eligibility_criteria: EligibilityCriteriaCreate) -> EligibilityCriteriaSchema:
    new_eligibility_criteria = await eligibility_criteria.create(db=session, obj_in=eligibility_criteria)
    await session.commit() 
    return new_eligibility_criteria

async def update_eligibility_criteria(session: Session, eligibility_criteria: EligibilityCriteriaCreate, eligibility_criteria_id: int) -> EligibilityCriteriaSchema:
    eligibility_criteria_in = await eligibility_criteria_crud.get(db=session, id=eligibility_criteria_id)
    if eligibility_criteria_in:
        upd_eligibility_criteria = await eligibility_criteria_crud.update(db=session, db_obj=eligibility_criteria_in, obj_in=eligibility_criteria)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Eligibility_criteria id: {eligibility_criteria_id} not found for update.") 
    await session.commit() 
    return upd_eligibility_criteria

async def get_eligibility_criteria_set(session):

    results = await eligibility_criteria_crud.get_eligibility_criteria_set(session)
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