from gearbox.schemas import SavedInputCreate, SavedInputPost, SavedInputSearchResults, SavedInputAll
from gearbox.models import SavedInput
from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from gearbox.crud.saved_input import saved_input_crud
from sqlalchemy import select, exc
from fastapi import HTTPException
from gearbox.util import status

async def get_latest_user_input(session: Session, user_id: int) -> SavedInputSearchResults:
    latest_saved_input = await saved_input_crud.get_latest_saved_input(session, user_id)
    if latest_saved_input:
        response = {
            "results": latest_saved_input.data,
            "id": latest_saved_input.id
        }
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Saved input not found for user '{user_id}'")
    return response

async def get_all_user_input(session: Session, user_id: int) -> SavedInputAll:
    # this method returns an array of saved inputs
    saved_inputs = await saved_input_crud.get_all_saved_input(session, user_id)
    saved_inputs = [{"filter": si.data, "id": si.id} for si in saved_inputs]

    response = {
        "results": saved_inputs,
        "id": user_id
    }
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
        "id": si.id
    }
    await session.commit()
    return response