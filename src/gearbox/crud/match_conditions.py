import datetime
from re import I
from sqlalchemy import func, update, select, exc

from gearbox.schemas.algorithm_engine import AlgorithmResponse
from sqlalchemy.orm import Session, joinedload

from gearbox.models import AlgorithmEngine, StudyAlgorithmEngine

from cdislogging import get_logger
logger = get_logger(__name__)

async def get_algorithm_engines(current_session: Session):

    stmt = select(AlgorithmEngine).options(
        joinedload(AlgorithmEngine.study_algo_engine).options(
            joinedload(StudyAlgorithmEngine.study_version)
        )
    ).order_by(AlgorithmEngine.sequence)
    result = await current_session.execute(stmt)
    ae = result.unique().scalars().all()
    return ae
