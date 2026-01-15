from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession as Session
from . import logger
from gearboxdatamodel.models import Value, Tag, CriterionHasValue, CriterionHasTag
from gearboxdatamodel.util import status
from gearboxdatamodel.schemas import CriterionSearchResults, CriterionCreateIn, CriterionCreate, CriterionHasValueCreate, CriterionHasTagCreate, DisplayRulesCreate, TriggeredByCreate, Criterion as CriterionSchema, CriterionStagingUpdate 
from gearboxdatamodel.crud import criterion_crud, criterion_has_value_crud, criterion_has_tag_crud, display_rules_crud, triggered_by_crud, value_crud, tag_crud
from gearbox.services import criterion_staging
from gearboxdatamodel.util.types import AdjudicationStatus
from typing import List

async def get_criterion(session: Session, id: int) -> CriterionSchema:
    crit = await criterion_crud.get(session, id)
    return crit

async def get_criteria(session: Session) -> CriterionSearchResults:
    aes = await criterion_crud.get_multi(session)
    return aes


async def create_new_criterion(session: Session, input_criterion_info: CriterionCreateIn, user_id: int) ->CriterionSchema:

    # keep track of any non-existent fks
    check_id_errors = []

    # triggered_by_value_id and triggered_by_criterion_id must both be populated or both null
    if not ((input_criterion_info.triggered_by_value_id == None) == (input_criterion_info.triggered_by_criterion_id == None)):
        check_id_errors.append('Input data must include both or neither triggered_by_value_id and triggered_by_criterion_id')
    elif input_criterion_info.triggered_by_value_id:
        check_id_errors.append(await value_crud.check_key(db=session, ids_to_check=input_criterion_info.triggered_by_value_id))
        check_id_errors.append(await criterion_crud.check_key(db=session, ids_to_check=input_criterion_info.triggered_by_criterion_id))

    if input_criterion_info.values:
        check_id_errors.append(await value_crud.check_key(db=session, ids_to_check=input_criterion_info.values))

    check_id_errors.append(await tag_crud.check_key(db=session, ids_to_check=input_criterion_info.tags))

    if not all(i is None for i in check_id_errors):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ERROR: missing FKs for criterion creation: {[error for error in check_id_errors if error]}")        

    # Build CriterionCreate object from input - exclude triggered_by, display_rules, tags, and values
    # which are separate inserts
    criterion_info_conv = jsonable_encoder(input_criterion_info)
    criterion_create = { key:value for key,value in criterion_info_conv.items() if key in CriterionCreate.model_fields.keys() }
    criterion_create = CriterionCreate(**criterion_create)
    new_criterion = await criterion_crud.create(db=session, obj_in=criterion_create)

    if input_criterion_info.values:
        for v_id in input_criterion_info.values:
            chv = CriterionHasValueCreate(criterion_id=new_criterion.id, value_id=v_id)
            new_value = await criterion_has_value_crud.create(db=session,obj_in=chv)

    # if it is determined that tags are not required, check if exists here before create 
    for t_id in input_criterion_info.tags:
        thv = CriterionHasTagCreate(criterion_id=new_criterion.id, tag_id=t_id)
        new_value = await criterion_has_tag_crud.create(db=session,obj_in=thv)

    dr = DisplayRulesCreate(criterion_id=new_criterion.id, 
        priority=input_criterion_info.display_rules_priority,
        version=input_criterion_info.display_rules_version
        )
    new_display_rule = await display_rules_crud.create(db=session, obj_in=dr)

    if input_criterion_info.triggered_by_criterion_id:
        tb = TriggeredByCreate(display_rules_id=new_display_rule.id,
            criterion_id=input_criterion_info.triggered_by_criterion_id,
            value_id=input_criterion_info.triggered_by_value_id,
            path=input_criterion_info.triggered_by_path
        )
        new_triggered_by = await triggered_by_crud.create(db=session, obj_in=tb)

    # After creating a new criterion, update criterion_staging
    # with the new criterion id and set status to ACTIVE
    if input_criterion_info.criterion_staging_id:
        criterion_staging_update = {
            "id": input_criterion_info.criterion_staging_id,
            "criterion_adjudication_status": AdjudicationStatus.ACTIVE,
            "criterion_id": new_criterion.id
        } 
        csu = CriterionStagingUpdate(**criterion_staging_update)
        csu_update = await criterion_staging.update(session, criterion=csu, user_id=user_id)

    # commit if no exceptions encountered 
    await session.commit()

    new_crit = await criterion_crud.get(session, id=new_criterion.id)
    return new_crit

async def update_criterion(session: Session, criterion: CriterionSchema) -> CriterionSchema:
    # TODO figure out the orm / DB issues going on with the scalar updates.
    criterion_to_upd = await criterion_crud.get(db=session, id=criterion.id)

    if not criterion_to_upd:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Criterion id {criterion.id} not found."
        )

    if criterion.values is not None:
        existing_value_ids = {v.value_id for v in criterion_to_upd.values}

        for wrapped in criterion.values:
            val = wrapped.value

            if not val:
                continue

            if getattr(val, "id", None):
                if val.id not in existing_value_ids:
                    existing_value = await session.get(Value, val.id)
                    criterion_to_upd.values.append(
                        CriterionHasValue(value=existing_value)
                    )
            else:
                new_value = Value(
                    description=val.description,
                    is_numeric=val.is_numeric,
                    value_string=val.value_string,
                    unit_id=val.unit_id,
                    operator=val.operator,
                    active=val.active,
                )
                session.add(new_value)
                await session.flush()

                criterion_to_upd.values.append(
                    CriterionHasValue(value=new_value)
                )

    if criterion.tags is not None:
        existing_tag_ids = {t.tag_id for t in criterion_to_upd.tags}

        for wrapped in criterion.tags:
            tag = wrapped.tag

            if not tag:
                continue

            if getattr(tag, "id", None):
                if tag.id not in existing_tag_ids:
                    existing_tag = await session.get(Tag, tag.id)
                    criterion_to_upd.tags.append(
                        CriterionHasTag(tag=existing_tag)
                    )
            else:
                new_tag = Tag(
                    code=tag.code,
                    type=tag.type
                )
                session.add(new_tag)
                await session.flush()

                criterion_to_upd.tags.append(
                    CriterionHasTag(tag=new_tag)
                )

    # scalar_update = criterion.model_dump(
    #     exclude_unset=True,
    #     exclude={"tags", "values"}
    # )

    # for field, value in scalar_update.items():
    #     setattr(criterion_to_upd, field, value)

    await session.commit()
    await session.refresh(criterion_to_upd)

    return criterion_to_upd


async def save_criterion(session: Session, criterion: CriterionCreate) -> CriterionSchema:
    new_criterion = await criterion_crud.create(db=session, obj_in=criterion)
    return new_criterion

async def get_criteria_not_exist_in_match_form(session: Session) -> List[CriterionSchema]:
    criteria = await criterion_crud.get_criteria_not_exist_in_match_form(db=session)
    return criteria