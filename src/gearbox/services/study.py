from . import logger
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import exc 
from fastapi import HTTPException
from gearbox.schemas import StudyCreate, StudySearchResults, Study as StudySchema, SiteHasStudyCreate, StudyUpdates
from gearbox.util import status
from gearbox.crud import study_crud, site_crud, site_has_study_crud, study_link_crud, site_has_study_crud, study_external_id_crud
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
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study for id: {study_id} not found for update.") 
    await session.commit() 
    return upd_study

async def update_studies(session: Session, updates: StudyUpdates):

    # Reset active to false for all rows in all study-related tables
    # TO DO: MODIFY THIS TO ONLY RESET STUDY INFORMATION
    # FOR STUDIES WITH SAME SOURCE AS INPUT DATA
    # THIS WILL HANDLE CASES WHERE WE ARE GETTING
    # STUDIES FROM A SOURCE OTHER THAN clinicaltrials.gov
    # --> WHAT ABOUT THE SAME STUDY COMING FROM 2 DIFFERENT SOURCES? 
    await study_crud.set_active_all_rows(db=session, active_upd=False)
    # WHAT ABOUT SITES FROM 2 DIFFERENT SOURCES? --> THAT IS COMMON TO BOTH?
#    await site_crud.set_active_all_rows(db=session, active_upd=False)
    await site_has_study_crud.set_active_all_rows(db=session, active_upd=False)
    await study_link_crud.set_active_all_rows(db=session, active_upd=False)

    for study in updates.studies:

        row = {
            'name':study.name,
            'code':study.code,
            'description':study.description,
            'active':study.active,
            'create_date': datetime.now()
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
        # if study is inactive then set all study_versions to inactive
        if not study.active:
            study_version.reset_active_status(session=session, study_id=new_or_updated_study_id)

        for site in study.sites:
            row = {
                'name': site.name,
                'code': site.code,
                'country': site.country,
                'city': site.city,
                'state': site.state,
                'zip': site.zip,
                'active': site.active,
                'create_date': datetime.now()
            }
            constraint_cols = [Site.code, Site.name]
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
                'active': site.active,
                'create_date': datetime.now()
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
                'active': link.active,
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