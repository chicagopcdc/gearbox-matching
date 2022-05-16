from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from gearbox.models.db import async_session

"""
def get_db() -> Generator:
     db = async_session()
     db.current_user_id = None
     try:
         yield db
     finally:
         db.close()
"""

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session