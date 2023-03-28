from . import logger
from gearbox.crud import el_criteria_has_criterion_crud
from gearbox.schemas import ElCriteriaHasCriterionCreate, ElCriteriaHasCriterionSearchResults, ElCriteriaHasCriterion as ElCriteriaHasCriterionSchema, ElCriteriaHasCriterions
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import select
from fastapi import HTTPException
from gearbox.util import status
from gearbox.models import ElCriteriaHasCriterion

async def get_el_criteria_has_criterion(session: Session, id: int) -> ElCriteriaHasCriterionSchema:
    ec = await el_criteria_has_criterion_crud.get(session, id)
    return ec

async def get_el_criteria_has_criterions(session: Session) -> ElCriteriaHasCriterionSearchResults: 
    ecs = await el_criteria_has_criterion_crud.get_multi(session)
    return ecs
    pass

async def find_duplicates_exist_in_db(session: Session, el_criteria_has_criterion: ElCriteriaHasCriterionCreate):

    echcs_in = el_criteria_has_criterion.echcs
    echc_ids = set([x.eligibility_criteria_id for x in el_criteria_has_criterion.echcs])

    echcs_db = []
    for eid in echc_ids:
        result = await session.execute(
                select(ElCriteriaHasCriterion).
                    where(ElCriteriaHasCriterion.eligibility_criteria_id == eid)
                )
        for echc in result.unique().scalars().all():
            echcs_db.append(echc)

    incoming_echcs = [
        {
            "criterion_id": x.criterion_id,
            "eligibility_criteria_id": x.eligibility_criteria_id,
            "value_id": x.value_id
         } for x in echcs_in 
    ]

    db_echcs = [
        {
            "criterion_id": x.criterion_id,
            "eligibility_criteria_id": x.eligibility_criteria_id,
            "value_id": x.value_id
         } for x in echcs_db
    ]

    echc_in_set = set(tuple(sorted(d.items())) for d in incoming_echcs)
    echc_db_set = set(tuple(sorted(d.items())) for d in db_echcs)
    duplicates = [dict(item) for item in (echc_in_set & echc_db_set)]

    if duplicates:
        logger.error(f"Following duplicate key values violate unique constraint on table EL_CRITERIA_HAS_CRITERION: {duplicates}")
        raise HTTPException(status.HTTP_409_CONFLICT, f"Following duplicate key values violate unique constraint on table EL_CRITERIA_HAS_CRITERION: {duplicates}")

# async def create_el_criteria_has_criterion(session: Session, el_criteria_has_criterion: ElCriteriaHasCriterionCreate) -> ElCriteriaHasCriterionSearchResults:
async def create_el_criteria_has_criterion(session: Session, el_criteria_has_criterion: ElCriteriaHasCriterionCreate) -> ElCriteriaHasCriterions:
    dupes = await find_duplicates_exist_in_db(session, el_criteria_has_criterion)
    echc_returned = []
    for echc in el_criteria_has_criterion.echcs:
        new_el_criteria_has_criterion = await el_criteria_has_criterion_crud.create(db=session, obj_in=echc)
        echc_returned.append(new_el_criteria_has_criterion)
    await session.commit() 
    return echc_returned

async def update_el_criteria_has_criterion(session: Session, el_criteria_has_criterion: ElCriteriaHasCriterionCreate, el_criteria_has_criterion_id: int) -> ElCriteriaHasCriterionSchema:
    el_criteria_has_criterion_in = await el_criteria_has_criterion_crud.get(db=session, id=el_criteria_has_criterion_id)
    if el_criteria_has_criterion_in:
        upd_el_criteria_has_criterion = await el_criteria_has_criterion_crud.update(db=session, db_obj=el_criteria_has_criterion_in, obj_in=el_criteria_has_criterion)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"el_criteria_has_criterion id: {el_criteria_has_criterion_id} not found for update.") 
    await session.commit() 
    return upd_el_criteria_has_criterion