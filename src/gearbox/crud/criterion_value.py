import datetime
from re import I
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session

from gearbox.models.models import Value


from cdislogging import get_logger
logger = get_logger(__name__)

async def get_values(current_session: Session):

    stmt = select(Value)

    result = await current_session.execute(stmt)
    ae = result.scalars().all()
    return ae
