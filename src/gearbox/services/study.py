from . import logger
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import HTTPException
from gearbox.schemas import StudyCreate, StudySearchResults, Study as StudySchema, SiteHasStudyCreate, StudyUpdates
from gearbox.util import status
from gearbox.crud import study_crud, site_crud, site_has_study_crud, study_link_crud, site_has_study_crud, study_external_id_crud, source_crud
from gearbox.models import Study, Site, StudyLink, SiteHasStudy, StudyExternalId
from gearbox.services import study_version

async def get_study_info(session: Session, id: int) -> StudySchema:
    aes = await study_crud.get_single_study_info(session, id)
    return aes

async def get_studies_info(session: Session) -> StudySearchResults:
    aes = await study_crud.get_studies_info(session)
    return aes
    pass

async def get_study(session: Session, id: int) -> StudySchema:
    aes = await study_crud.get(session, id)
    return aes

async def get_studies(session: Session) -> StudySearchResults:
    aes = await study_crud.get_multi(session)
    return aes

async def create_study(session: Session, study: StudyCreate) -> StudySchema:

    sites = study.sites
    links = study.links
    new_study = await study_crud.create(db=session, obj_in=study)

    if sites:
        new_site_ids = []
        for site in sites:
            new_site = await site_crud.create(db=session, obj_in=site)
            new_site_ids.append(new_site.id)

        for site_id in new_site_ids:
            shs = SiteHasStudyCreate(study_id=new_study.id, site_id=site_id, active=True)
            new_shs = await site_has_study_crud.create(db=session, obj_in=shs)
    
    if links:
        for link in links:
            link.study_id = new_study.id
            new_link = await study_link_crud.create(db=session, obj_in=link)
    
    await session.commit()
    return new_study

async def update_study(session: Session, study: StudyCreate, study_id: int) -> StudySchema:
    study_in = await study_crud.get(db=session, id=study_id)
    if study_in:
        upd_study = await study_crud.update(db=session, db_obj=study_in, obj_in=study)
    else:
        logger.error(f"ERROR: Study for id: {study_id} not found for update.")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study for id: {study_id} not found for update.") 
    await session.commit() 
    return upd_study

async def update_studies(session: Session, updates: StudyUpdates):

    source = updates.source
    source_id = await source_crud.get_id(db=session, source=source)
    if not source_id:
        logger.error(f"ERROR: refresh study info source: {source} does not exist in source table.")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Error: refresh study info source: {source} does not exist")


    source_study_ids = await study_crud.get_study_ids_for_source(db=session, source=source)
    # Reset active to false for all rows in all study-related tables
    # For studies coming from the same source
    source = updates.source
    await study_crud.set_active_all_rows(db=session, active_upd=False, ids=source_study_ids)
    await site_has_study_crud.set_active_all_rows(db=session, active_upd=False, ids=source_study_ids)
    await study_link_crud.set_active_all_rows(db=session, active_upd=False, ids=source_study_ids)

    priority = await source_crud.get_priority(db=session, source=source)

    # get a list of existing studies
    existing_studies = await study_crud.get_existing_studies(db=session)

    # get new studies
    incoming_studies = []
    for study in updates.studies:
        incoming_studies.append(study.code)

    new_studies = [ x for x in incoming_studies if x not in existing_studies]

    # get study.code for all studies at the same or lower priority
    studies_to_update = await study_crud.get_studies_for_update(db=session, priority=priority)
    studies_to_update.extend(new_studies)

    for study in updates.studies:
        if study.code in studies_to_update:

            row = {
                'name':study.name,
                'code':study.code,
                'description':study.description,
                'active':study.active,
                'create_date': datetime.now(),
                'source_id': source_id
            }
            no_update_cols = ['create_date']
            constraint_cols = [Study.code]
            new_or_updated_study_id = await study_crud.upsert(
                db=session, 
                model=Study, 
                row=row, 
                as_of_date_col='create_date', 
                no_update_cols=no_update_cols, 
                constraint_cols=constraint_cols
            )

            for site in study.sites:
                row = {
                    'name': site.name,
                    'country': site.country,
                    'city': site.city,
                    'state': site.state,
                    'zip': site.zip,
                    'create_date': datetime.now(),
                    'source_id': source_id
                }
                # name / zipcode are unique to site
                constraint_cols = [Site.name, Site.zip]
                no_update_cols=['create_date']
                new_or_updated_site_id = await site_crud.upsert(
                    db=session, 
                    model=Site, 
                    row=row, 
                    as_of_date_col='create_date', 
                    no_update_cols=no_update_cols, 
                    constraint_cols=constraint_cols
                )

                row = {
                    'study_id': new_or_updated_study_id,
                    'site_id': new_or_updated_site_id,
                    'create_date': datetime.now(),
                    'active': study.active
                }
                no_update_cols = ['create_date']
                constraint_cols = [Site.id, Study.id]
                new_or_updated_site_has_study_id = await site_has_study_crud.upsert(
                    db=session, 
                    model=SiteHasStudy, 
                    row=row, 
                    as_of_date_col='create_date', 
                    no_update_cols=no_update_cols
                )

            for link in study.links:
                row = {
                    'name': link.name,
                    'href': link.href,
                    'study_id' : new_or_updated_study_id,
                    'active': study.active,
                    'create_date': datetime.now()
                }
                no_update_cols = ['create_date']
                constraint_cols = [StudyLink.study_id, StudyLink.href]
                new_or_updated_link_id = await study_link_crud.upsert(
                    db=session, 
                    model=StudyLink, 
                    row=row, 
                    no_update_cols=no_update_cols, 
                    constraint_cols=constraint_cols
                )

            for ext_id in study.ext_ids:
                row = {
                    'study_id' : new_or_updated_study_id,
                    'ext_id': ext_id.ext_id,
                    'source': ext_id.source,
                    'source_url': ext_id.source_url,
                    'active': ext_id.active,
                    'create_date': datetime.now()
                }
                no_update_cols = ['create_date']
                constraint_cols = [StudyExternalId.study_id, StudyExternalId.ext_id]
                new_or_updated_ext_id = await study_external_id_crud.upsert(
                    db=session, 
                    model=StudyExternalId, 
                    row=row, 
                    no_update_cols=no_update_cols, 
                    constraint_cols=constraint_cols
                )

    return True

def get_new_version(study_info: dict) -> str:
    ts = datetime.now().strftime('%m-%d-%Y:%H-%M-%S')
    version = 1
    if isinstance(study_info, dict): 
        current_version = study_info.get("version")
        if current_version:
            version = int(current_version.split(":")[0]) + 1
    return str(version) + ':' + ts

