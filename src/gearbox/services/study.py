from . import logger
from datetime import datetime
from gearbox import config
from fastapi.encoders import jsonable_encoder
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import HTTPException, Request
from gearboxdatamodel.schemas import StudyCreate, StudySearchResults, Study as StudySchema, SiteHasStudyCreate, StudyUpdates, StudyResults
from gearbox.util import bucket_utils
from gearboxdatamodel.util import status
from gearboxdatamodel.util.types import StudyVersionStatus
from gearboxdatamodel.crud import study_crud, site_crud, site_has_study_crud, study_link_crud, site_has_study_crud, study_external_id_crud, source_crud, study_version_crud
from gearboxdatamodel.models import Study, Site, StudyLink, SiteHasStudy, StudyExternalId, StudyVersion
from operator import itemgetter
from gearbox.services import match_conditions as mc, match_form as mf, eligibility_criteria as ec

async def get_study_info(session: Session, id: int) -> StudySchema:
    study_info = await study_crud.get_single_study_info(session, id)
    if study_info:
        return study_info
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Study for id: {id} not found.") 

async def get_studies_info(session: Session) -> StudySearchResults:
    studies = await study_crud.get_studies_info(session)
    return studies
    pass

async def get_study_id_by_ext_id(session: Session, ext_id: str) -> int:
    study_id = await study_external_id_crud.get_study_id_by_ext_id(session, ext_id)
    return study_id

async def get_study(session: Session, id: int) -> StudySchema:
    study = await study_crud.get(session, id)
    if study:
        return study
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Study for id: {study_id} not found.") 

async def get_studies(session: Session) -> StudySearchResults:
    studies = await study_crud.get_multi(session)
    return studies

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

async def update_study(session: Session, study: StudyCreate, study_id: int, noload_rel:List=None) -> StudySchema:
    study_in = await study_crud.get(db=session, id=study_id, noload_rel=noload_rel)
    if study_in:
        upd_study = await study_crud.update(db=session, db_obj=study_in, obj_in=study)
    else:
        logger.error(f"ERROR: Study for id: {study_id} not found for update.")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study for id: {study_id} not found for update.") 
    await session.commit() 
    return upd_study

async def get_studies_to_update(existing_studies: list[Study], refresh_studies: list[StudyCreate]):
    """
    This function compares incoming refresh studies to studies existing
    in the database. It returns a list of study codes that do not 
    have an exact match for all study fields existing in the database.
    The purpose of the function is to reduce the number of upsert operations
    required for the update studies (refresh) process. 
    """

    studies_to_update = []
    existing = [{'name':x.name, 
                               'code':x.code, 
                               'description': x.description,
                               'links': [{'name':y.name,'href':y.href} for y in x.links],
                               'sites': [{'name':z.site.name, 
                                          'country':z.site.country,
                                          'city':z.site.city,
                                          'state':z.site.state,
                                          'zip':z.site.zip,
                                          'location_lat': z.site.location_lat,
                                          'location_long': z.site.location_long
                                          } for z in x.sites],
                                'ext_ids': [{'ext_id':a.ext_id,
                                             'source':a.source,
                                             'source_url':a.source_url} for a in x.ext_ids]
                               } for x in existing_studies]

    refresh = [{'name':x.name, 
                               'code':x.code, 
                               'description': x.description,
                               'links': [{'name':y.name,'href':str(y.href)} for y in x.links],
                               'sites': [{'name':z.name, 
                                          'country':z.country, 'city':z.city,
                                          'state':z.state,
                                          'zip':z.zip,
                                          'location_lat': z.location_lat,
                                          'location_long': z.location_long
                                          } for z in x.sites],
                                'ext_ids': [{'ext_id':a.ext_id,
                                             'source':a.source,
                                             'source_url':str(a.source_url)} for a in x.ext_ids]
                               } for x in refresh_studies]
    
    existing = sorted(existing, key=itemgetter('code'))
    refresh = sorted(refresh, key=itemgetter('code'))

    for i in refresh:
        # if a refresh study is not an exact match
        # for an existing study
        if i not in existing:
            studies_to_update.append(i.get('code'))


    return studies_to_update

async def update_studies(session: Session, request:Request, updates: StudyUpdates, update_fe: bool=True):
    """
    Comments: This function does a refresh of the study, study_links, study_external_ids,
        site_has_study, and site tables. Rather than delete the existing information,
        the 'active' flag is set to false for all studies that do not exist in the
        studyupdates json document. The function will also update the json files used
        by the frontend if update_files. 
    """

    # Get / validate the updates source
    source = updates.source
    source_id = await source_crud.get_id(db=session, source=source)
    if not source_id:
        logger.error(f"ERROR: refresh study info source: {source} does not exist in source table.")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Error: refresh study info source: {source} does not exist")

    # Get study ids of all studies that exist in the db for the source
    source_study_ids = await study_crud.get_study_ids_for_source(db=session, source=source)

    # Reset active to false for all rows in all study-related tables
    # For incoming studies from the same source
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

    # get all studies in the db for the same or lower priority
    existing_studies = await study_crud.get_studies_for_update(db=session, priority=priority)

    # get study codes for all studies that require upsert
    # this function returns all studies in the incoming data
    # that contain updates to existing studies or new studies
    study_codes_to_update = await get_studies_to_update(existing_studies=existing_studies, refresh_studies=updates.studies)
    study_ids_reset_to_active = []

    for study in updates.studies:

        if study.code not in study_codes_to_update:
            study_id = await study_crud.get_study_id_by_code(current_session=session , study_code=study.code)
            if study_id:
                study_ids_reset_to_active.append(study_id)

        else:
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
            new_or_updated_study = await study_crud.upsert(
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
                    'location_lat': site.location_lat,
                    'location_long': site.location_long,
                    'create_date': datetime.now(),
                    'source_id': source_id
                }

                # name / zipcode are unique to site
                constraint_cols = [Site.name, Site.zip]
                no_update_cols=['create_date']
                new_or_updated_site = await site_crud.upsert(
                    db=session, 
                    model=Site, 
                    row=row, 
                    as_of_date_col='create_date', 
                    no_update_cols=no_update_cols, 
                    constraint_cols=constraint_cols
                )

                row = {
                    'study_id': new_or_updated_study.id,
                    'site_id': new_or_updated_site.id,
                    'create_date': datetime.now(),
                    'active': study.active
                }
                no_update_cols = ['create_date']
                constraint_cols = [Site.id, Study.id]
                new_or_updated_site_has_study = await site_has_study_crud.upsert(
                    db=session, 
                    model=SiteHasStudy, 
                    row=row, 
                    as_of_date_col='create_date', 
                    no_update_cols=no_update_cols
                )

            for link in study.links:
                row = {
                    'name': link.name,
                    'href': str(link.href),
                    'study_id' : new_or_updated_study.id,
                    'active': study.active,
                    'create_date': datetime.now()
                }
                no_update_cols = ['create_date']
                constraint_cols = [StudyLink.study_id, StudyLink.href]
                new_or_updated_link = await study_link_crud.upsert(
                    db=session, 
                    model=StudyLink, 
                    row=row, 
                    no_update_cols=no_update_cols, 
                    constraint_cols=constraint_cols
                )

            for ext_id in study.ext_ids:
                row = {
                    'study_id' : new_or_updated_study.id,
                    'ext_id': ext_id.ext_id,
                    'source': ext_id.source,
                    'source_url': str(ext_id.source_url),
                    'active': ext_id.active,
                    'create_date': datetime.now()
                }
                no_update_cols = ['create_date']
                constraint_cols = [StudyExternalId.ext_id]
                new_or_updated_ext_id = await study_external_id_crud.upsert(
                    db=session, 
                    model=StudyExternalId, 
                    row=row, 
                    no_update_cols=no_update_cols, 
                    constraint_cols=constraint_cols
                )

    # Expire all objects after upserts. This is needed in order to keep the
    # ORM and db in sync.
    session.expire_all()

    # Reset to active all study_ids that were in the incoming updates 
    # but did not have any changes
    await study_crud.set_active_all_rows(db=session, active_upd=True, ids=study_ids_reset_to_active)
    await site_has_study_crud.set_active_all_rows(db=session, active_upd=True, ids=study_ids_reset_to_active)
    await study_link_crud.set_active_all_rows(db=session, active_upd=True, ids=study_ids_reset_to_active)

    ## Set any 'ACTIVE' study versions to 'INACTIVE' for all inactive studies
    noload = [Study.patients, Study.sites, Study.links, Study.ext_ids, Study.study_versions, Study.study_source] 
    noload_sv = [StudyVersion.eligibility_criteria, StudyVersion.study_algorithm_engine, StudyVersion.study]
    inactive_studies = await study_crud.get_multi(db=session, active=False, noload_rel=noload)
    for inactive_study in inactive_studies:

        where_clause=[f"study_id = {inactive_study.id}", f"status = '{StudyVersionStatus.ACTIVE.value}'"]
        svs = await study_version_crud.get_multi(session, 
            noload_rel = noload_sv,
            where=where_clause)

        for sv in svs:
            await study_version_crud.update(db=session, db_obj=sv, obj_in={"status":StudyVersionStatus.INACTIVE.value})

    if update_fe:
        await refresh_study_fe_files(session=session, request=request)

    return True

def get_new_version(study_info: dict) -> str:
    ts = datetime.now().strftime('%m-%d-%Y:%H-%M-%S')
    version = 1
    if isinstance(study_info, dict): 
        current_version = study_info.get("version")
        if current_version:
            version = int(current_version.split(":")[0]) + 1
    return str(version) + ':' + ts


async def build_studies(session: Session, request: Request) -> StudySchema:

    results = await get_studies_info(session)
    bucket_name = bucket_utils.get_bucket_name()
    existing_studies = bucket_utils.get_object(request=request, bucket_name=bucket_name, key_name=config.S3_BUCKET_STUDIES_KEY_NAME, expires=300, method="get_object")
    version = get_new_version(existing_studies)
    studies = [StudySchema.model_validate(obj=study_obj, from_attributes=True) for study_obj in results]
    new_studies = StudyResults(version=version, studies=studies)

    #Remove inactive study links
    for study in new_studies.studies:
        study.links = [x for x in study.links if x.active]

    if not config.BYPASS_S3:
        json_studies = jsonable_encoder(new_studies)
        params = [{'Content-Type':'application/json'}]
        bucket_utils.put_object(request, bucket_name, config.S3_BUCKET_STUDIES_KEY_NAME, config.S3_PUT_OBJECT_EXPIRES, params, json_studies)

    return new_studies

async def refresh_study_fe_files(session: Session, request: Request):

    await build_studies(session=session, request=request)
    await mc.build_match_conditions(session=session, request=request)
    await mf.build_match_form(session=session, request=request, save=True)
    await ec.build_eligibility_criteria(session=session, request=request)
