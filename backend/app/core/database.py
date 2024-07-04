from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.settings import settings


engine: AsyncEngine = create_async_engine(
    url=settings.database.url,
    poolclass=NullPool,
    echo=settings.database.echo,
)

session: AsyncSession = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def close_db_connection() -> None:
    await engine.dispose()
