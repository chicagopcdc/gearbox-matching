from gearbox.schemas import SavedInputCreate, SavedInputPost, SavedInputSearchResults 
from gearbox.models import SavedInput
from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from gearbox.crud.saved_input import saved_input_crud
from sqlalchemy import select, exc
from fastapi import HTTPException
from gearbox.util import status
from typing import List
from gearbox.services.criterion import get_criteria
import asyncio
import time
from aiocache import cached, Cache, caches
from aiocache.serializers import JsonSerializer
import json


async def reset_user_validation_data():
    try:
        # Get the cache instance
        cache = caches.get('default')  # Assuming the cache is named 'MEMORY'

        # Clear the cache for the specific key
        await cache.delete('update_user_validation_data')
        
    except Exception as e:
        logger.error(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "something went wrong when clearing validation data check logs")

@cached(key='update_user_validation_data')
async def update_user_validation_data(session: Session) -> dict:
    logger.info("User input validation data update STARTING")
    valid_criterion_format = {}
    try:
        #valid_criterion_format = {} #{id: {"display_name": "input_type": "values": "constraints":}}
        criteria = await get_criteria(session)
        
        for criterion in criteria:
            valid_criterion_format[str(criterion.id)] = {
                "display_name": criterion.display_name, 
                "input_type": criterion.input_type.data_type, 
                "values": set(value.value_id for value in criterion.values) if criterion.values else None,
                "constraints": None 
            }
    except Exception as e:
        logger.error(f"User input validation ran into an ERROR: {e}")
        logger.error(f"Maintaining previous validation Data")

    logger.info("User input validation update COMPLETED")
    return valid_criterion_format


async def validate_user_input(session: Session, user_input: dict) -> bool:
    valid_criterion_format = await update_user_validation_data(session)
    def error_message(input, display_name=None, input_type=None, values=None, id=None,):
        message = f'incorrect format in input: {input}.'

        #id does not exist
        if id:
            message += f" the id {id} in does not match any criterion"
        
        #value input_type error
        if display_name:
            message += f" the value given for: '{display_name}'"
            if input_type: 
                message += f" must be a{'n integer' if input_type == 'list' else ' string'}{' containing an integer' if input_type.lower() == 'integer' else ' containing a floating point number' if input_type == 'Float' or input_type == 'percentage'  else ''}"
            if values:
                message += f" is not one of the valid options: {values}"
            

        raise HTTPException(status.HTTP_400_BAD_REQUEST, message)

    if not valid_criterion_format:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "the validation data has not been setup or failed, user-input cannot be submitted")

    for input in user_input:
        
        if (len(input) != 2
            or "id" not in input 
            or "value" not in input 
            or not isinstance(input["id"], int)
            or (not isinstance(input["value"], str) and not isinstance(input["value"], int)) 
            ):
            error_message(input)

        id = str(input["id"])
        value = input["value"]

        if id in valid_criterion_format:
            
            criterion = valid_criterion_format[id]
            display_name = criterion["display_name"]
            input_type = criterion["input_type"]
            options = criterion['values']

            if input_type == 'list':
                if not isinstance(value, int):
                    error_message(input, display_name, input_type)
                
                if value not in options:
                    error_message(input, display_name, values=options)
        
            else:

                if not isinstance(value, str):
                    error_message(input, display_name, input_type)

                if input_type.lower() == "integer":
                    try:
                        int(value)
                    except ValueError:
                        error_message(input, display_name, input_type)
                
                else:
                    try:
                        float(value)
                    except ValueError:
                        error_message(input, display_name, input_type)
                
        else:
            error_message(input, id=id)



async def get_latest_user_input(session: Session, user_id: int) -> SavedInputSearchResults:
    latest_saved_input = await saved_input_crud.get_latest_saved_input(session, user_id)
    response = {
        "results": [{}] if not latest_saved_input else latest_saved_input.data,
        "id": user_id if not latest_saved_input else latest_saved_input.id
    }
    return response

async def get_all_user_input(session: Session, user_id: int) -> List[SavedInputSearchResults]:
    # this method returns an array of saved inputs
    saved_inputs = await saved_input_crud.get_all_saved_input(session, user_id)
    saved_inputs = [{"results": si.data, "id": si.id, "name": si.name} for si in saved_inputs]
    response = saved_inputs
    return response


async def create_saved_input(session: Session, user_input: SavedInputCreate, user_id: int) -> SavedInputSearchResults:
    uid = dict(user_input)
    uid['user_id'] = user_id
    user_input_post = SavedInputPost(**uid)
    if not user_input_post.id:
        si = await saved_input_crud.create(db=session,  obj_in=user_input_post)
    else:
        stmt = select(SavedInput).where(SavedInput.id == user_input_post.id, SavedInput.user_id == user_id).with_for_update(nowait=True)
        stmt.execution_options(synchronize_session="fetch")
        try:
            result = await session.execute(stmt)
            saved_input = result.scalars().first()
        except exc.SQLAlchemyError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}")        

        si = await saved_input_crud.update(db=session, db_obj=saved_input, obj_in=user_input_post)

    response = {
        "results": si.data,
        "id": si.id,
        "name": si.name
    }
    await session.commit()
    return response
