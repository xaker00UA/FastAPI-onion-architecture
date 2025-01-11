from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from .config import settings
from sqlalchemy import AsyncAdaptedQueuePool, NullPool
import asyncio

engine = create_async_engine(
    settings.db_dsn,
    poolclass=NullPool if settings.mode == "TEST" else AsyncAdaptedQueuePool,
    echo=False,
)


class Base(DeclarativeBase):
    pass


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        tables = Base.metadata.tables.keys()
        for table_name in tables:
            # Формируем запрос для удаления каждой таблицы с CASCADE
            await conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE;"))
        # await conn.run_sync(Base.metadata.drop_all)
