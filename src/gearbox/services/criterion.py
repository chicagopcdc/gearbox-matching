from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from . import logger
from gearboxdatamodel.models import Value, Tag, CriterionHasValue, CriterionHasTag
from gearboxdatamodel.util import status
from gearboxdatamodel.schemas import CriterionSearchResults, CriterionCreateIn, CriterionCreate, CriterionHasValueCreate, CriterionHasTagCreate, DisplayRulesCreate, TriggeredByCreate, Criterion as CriterionSchema, CriterionStagingUpdate, CriterionUpdate, CriterionUpdateIn 
from gearboxdatamodel.crud import criterion_crud, criterion_has_value_crud, criterion_has_tag_crud, display_rules_crud, triggered_by_crud, value_crud, tag_crud
from gearbox.services import criterion_staging
from gearboxdatamodel.util.types import AdjudicationStatus
from typing import List



async def get_criterion(session: Session, id: int) -> CriterionSchema:
    crit = await criterion_crud.get(session, id)
    return crit

async def get_criteria(session: Session, include_studies: bool = False, where: List[str] = None) -> CriterionSearchResults:

    if where:
        aes = await criterion_crud.get_multi(db=session, where=where)
    else:
        aes = await criterion_crud.get_multi(session)
    
    if include_studies:
        # Fetch studies for each criterion
        for criterion in aes:
            studies = await criterion_crud.get_studies_for_criterion(session, criterion.id)
            criterion.studies = studies
    return aes

async def get_studies_for_criterion(session: Session, criterion_id: int):
    return await criterion_crud.get_studies_for_criterion(session, criterion_id)


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

async def update_criterion(session: Session, criterion: CriterionUpdate, user_id: int) -> CriterionSchema:
    logger.info(criterion)
    criterion_to_upd = await criterion_crud.get(db=session, id=criterion.id)
    if not criterion_to_upd:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Criterion id {criterion.id} not found."
        )

    update_in = CriterionUpdateIn.model_validate(
        criterion.model_dump(exclude_unset=True)
    )
    scalar_data = update_in.model_dump(
        exclude_unset=True,
        mode="python",
    )
    for field, value in scalar_data.items():
        logger.info(f"Updating field {field} to value {value}")
        setattr(criterion_to_upd, field, value)
        

    if criterion.values is not None:
        existing_value_ids = {v.value_id for v in criterion_to_upd.values}
        logger.info(f"Existing value IDs: {existing_value_ids}")

        for val in criterion.values:
            try:
                if getattr(val, "id", None):
                    if val.id not in existing_value_ids:
                        existing_value = await session.get(Value, val.id)
                        if not existing_value:
                            logger.error(f"Value {val.id} not found in database. Value not added to criterion {criterion_to_upd.id}")
                            continue

                        logger.info(f"Adding existing value {val.id} to criterion {criterion_to_upd.id}")
                        assoc = CriterionHasValue(
                            criterion_id=criterion_to_upd.id,
                            value_id=val.id
                        )
                        session.add(assoc)  
                        logger.info(f"Added value {val.id} to criterion {criterion_to_upd.id}")
                    else:
                        logger.info(f"Value {val.id} already associated, skipping")
                else:
                    logger.info(f"Creating new value: {val.value_string}, numeric={val.is_numeric}, unit={val.unit_id}, op={val.operator}")

                    existing_check = await session.execute(
                        select(Value).where(
                            Value.is_numeric == val.is_numeric,
                            Value.unit_id == val.unit_id,
                            Value.value_string == val.value_string,
                            Value.operator == val.operator
                        )
                    )
                    existing_value = existing_check.scalar_one_or_none()
                    if existing_value:
                        logger.info(f"Value already exists with id {existing_value.id}, using it")
                        value_id_to_use = existing_value.id
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
                        value_id_to_use = new_value.id
                        logger.info(f"New value created with id {value_id_to_use}")

                    
                    if value_id_to_use not in existing_value_ids:
                        assoc = CriterionHasValue(
                            criterion_id=criterion_to_upd.id,
                            value_id=value_id_to_use
                        )
                        session.add(assoc)
                        logger.info(f"Added value {value_id_to_use} to criterion {criterion_to_upd.id}")
                    else:
                        logger.info(f"Value {value_id_to_use} already associated, skipping")

            except IntegrityError as e:
                logger.error(f"IntegrityError on value {val}: {e}")
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Database constraint violation: {str(e)}"
                )
            except Exception as e:
                logger.error(f"Unexpected error on value {val}: {e}", exc_info=True)
                raise

    if criterion.tags is not None:
        existing_tag_ids = {t.tag_id for t in criterion_to_upd.tags}
        logger.info(f"Existing tag IDs: {existing_tag_ids}")

        for t in criterion.tags:
            try:
                if getattr(t, "id", None):
                    if t.id not in existing_tag_ids:
                        existing_value = await session.get(Tag, t.id)
                        if not existing_value:
                            logger.error(f"Tag {t.id} not found in database. Tag not added to criterion {criterion_to_upd.id}")
                            continue

                        logger.info(f"Adding existing tag {t.id} to criterion {criterion_to_upd.id}")
                        assoc = CriterionHasTag(
                            criterion_id=criterion_to_upd.id,
                            tag_id=t.id
                        )
                        session.add(assoc)  
                        logger.info(f"Added tag {t.id} to criterion {criterion_to_upd.id}")
                    else:
                        logger.info(f"Tag {t.id} already associated, skipping")
                else:
                    logger.info(f"Creating new tag: code={t.code}, type={t.type}")

                    existing_check = await session.execute(
                        select(Tag).where(
                            Tag.code == t.code,
                            Tag.type == t.type
                        )
                    )
                    existing_value = existing_check.scalar_one_or_none()
                    if existing_value:
                        logger.info(f"Tag already exists with id {existing_value.id}, using it")
                        value_id_to_use = existing_value.id
                    else:
                        new_tag = Tag(
                            code=t.code,
                            type=t.type
                        )
                        session.add(new_tag)
                        await session.flush()

                        value_id_to_use = new_tag.id
                        logger.info(f"New tag created with id {value_id_to_use}")

                    
                    if value_id_to_use not in existing_tag_ids:
                        assoc = CriterionHasTag(
                            criterion_id=criterion_to_upd.id,
                            tag_id=value_id_to_use
                        )
                        session.add(assoc)
                        logger.info(f"Added tag {value_id_to_use} to criterion {criterion_to_upd.id}")
                    else:
                        logger.info(f"Tag {value_id_to_use} already associated, skipping")
            except IntegrityError as e:
                logger.error(f"IntegrityError on tag {t}: {e}")
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Database constraint violation: {str(e)}"
                )
            except Exception as e:
                logger.error(f"Unexpected error on tag {val}: {e}", exc_info=True)
                raise

    logger.info(f"Total values in relationship before commit: {len(criterion_to_upd.values)}")
    logger.info(f"Total tags in relationship before commit: {len(criterion_to_upd.tags)}")
    await session.commit()
    logger.info("Commit completed")
    await session.refresh(criterion_to_upd)
    logger.info(f"Total values in relationship after refresh: {len(criterion_to_upd.values)}")
    logger.info(f"Total values in relationship after refresh: {len(criterion_to_upd.tags)}")

    # Update existing criterion staging records with the udpated information from this criteria
    await criterion_staging.refresh_criterion_staging(session, criterion_to_upd, user_id)

    return criterion_to_upd


async def save_criterion(session: Session, criterion: CriterionCreate) -> CriterionSchema:
    new_criterion = await criterion_crud.create(db=session, obj_in=criterion)
    return new_criterion

async def get_criteria_not_exist_in_match_form(session: Session) -> List[CriterionSchema]:
    criteria = await criterion_crud.get_criteria_not_exist_in_match_form(db=session)
    return criteria
