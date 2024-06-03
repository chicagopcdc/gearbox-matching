from sqlalchemy.ext.asyncio import AsyncSession as Session
from gearbox.schemas import InputTypeSearchResults
from gearbox.crud import input_type_crud


async def get_input_types(session: Session) -> InputTypeSearchResults:
    aes = await input_type_crud.get_multi(session)
    return aes