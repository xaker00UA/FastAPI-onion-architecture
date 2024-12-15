from contextlib import asynccontextmanager
from typing import Callable, Optional, Generic, AsyncGenerator
from pydantic import BaseModel
from sqlalchemy import select
from app.configurations.database import Base
from app.configurations.context_manager import get_db, SessionLocal

from sqlalchemy.ext.asyncio import AsyncSession


class BaseCrud:
    model: Base

    def __init__(self):
        # self.get_db: Callable[[], AsyncGenerator[AsyncSession, None]] = get_db
        pass

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with SessionLocal() as session:  # Асинхронный контекст сессии
            yield session

    async def add(self, obj) -> int:
        async with self.get_session() as ses:
            model = self.model(**obj.model_dump())  # Преобразуем схему в модель
            ses.add(model)  # Добавляем объект в сессию
            await ses.commit()  # Фиксируем изменения
            await ses.refresh(model)  # Обновляем объект после коммита
            return model.id

    async def get_all(self) -> list[Base] | None:
        async with self.get_session() as ses:
            result = await ses.execute(select(self.model))
            return result.scalars().all()

    async def get_by_id(self, id) -> Base | None:
        async with self.get_session() as ses:
            result = await ses.execute(select(self.model).filter(self.model.id == id))
            return result.scalars().first()

    async def delete_by_id(self, id) -> bool:
        async with self.get_session() as ses:
            result = await ses.execute(select(self.model).filter(self.model.id == id))
            instance = result.scalars().first()
            if instance:
                await ses.delete(instance)
                await ses.commit()
                return True
            return False

    async def update_by_id(self, id, obj) -> int | None:
        async with self.get_session() as ses:
            result = await ses.execute(select(self.model).filter(self.model.id == id))
            model = result.scalars().first()
            if model:
                for key, value in obj.model_dump().items():
                    setattr(model, key, value)
                await ses.commit()
                await ses.refresh(model)
                return model.id
            return None
