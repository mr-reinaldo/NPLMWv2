from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session() as db_session:
        yield db_session
