from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .db import engine


SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=True,
)


async def get_db():
    async with SessionLocal() as session:  # Асинхронный контекст сессии
        yield session
