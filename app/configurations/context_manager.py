from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from .config import settings
import os
import logging


# test_engine = create_async_engine(settings.test_db, echo=False)
# SessionLocal = sessionmaker(
#     expire_on_commit=False, class_=AsyncSession, bind=test_engine
# )


engine = create_async_engine(settings.db_dsn, echo=False)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_db():
    async with SessionLocal() as session:  # Асинхронный контекст сессии
        yield session
