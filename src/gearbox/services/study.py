from . import logger
from sqlalchemy.orm import Session
from sqlalchemy import exc 
from fastapi import HTTPException
from gearbox.schemas import StudyCreate, StudySearchResults, Study as StudySchema, SiteHasStudyCreate
from gearbox.util import status
from gearbox.crud import study_crud, site_crud, site_has_study_crud, study_link_crud

async def get_study_info(session: Session, id: int) -> StudySchema:
    aes = await study_crud.get_study_info(session, id)
    return aes

async def get_studies_info(session: Session) -> StudySearchResults:
    aes = await study_crud.get_studies_info(session)
    return aes
    pass

async def get_study(session: Session, id: int) -> StudySchema:
    aes = await study_crud.get_study(session, id)
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
    
    session.commit()
    return new_study

async def update_study(session: Session, study: StudyCreate, study_id: int) -> StudySchema:
    study_in = await study_crud.get(db=session, id=study_id)
    if study_in:
        upd_study = await study_crud.update(db=session, db_obj=study_in, obj_in=study)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study for id: {study_id} not found for update.") 
    await session.commit() 
    return upd_study