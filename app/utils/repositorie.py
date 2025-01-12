from abc import ABC, abstractmethod

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from ..configurations.context_manager import get_db
from fastapi import HTTPException


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def edit_one():
        raise NotImplementedError

    @abstractmethod
    async def find_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None
    name_repo = "base_repo"

    def __new__(cls, *args, **kwargs):
        # Проверяем, что дочерний класс определил model
        if cls.model is None:
            raise TypeError(f"Class {cls.__name__} must define the 'model' attribute.")

        # Проверяем, что дочерний класс определил name_repo
        if cls.name_repo == "base_repo":
            raise TypeError(
                f"Class {cls.__name__} must define the 'name_repo' attribute."
            )

        return super().__new__(cls)

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return {"id": res.scalar_one()}

    async def edit_one(self, id: int, data: dict) -> int:
        stmt = (
            update(self.model)
            .values(**data)
            .where(self.model.id == id)  # Используйте filter вместо filter_by
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)

        # Возвращаем id или None, если запись не найдена
        return {"id": result.scalar_one_or_none()}

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.unique().all()]
        return res

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.unique().scalar_one_or_none()
        if res:
            res = res.to_read_model()
        return res

    async def delete_one(self, id: int) -> int:
        try:
            stmt = delete(self.model).where(self.model.id == id).returning(self.model)
            res = await self.session.execute(stmt)
            res = res.scalar_one_or_none()
            if res:
                res = res.to_read_model()
            return res
        except IntegrityError:
            raise HTTPException(
                status_code=409, detail="Cannot delete model due to links"
            )
