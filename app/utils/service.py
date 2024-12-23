from abc import ABC, abstractmethod
from .unittowork import UnitOfWork, IUnitOfWork
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.responses import JSONResponse, Response, ORJSONResponse


class ServiceAbstract(ABC):
    @abstractmethod
    def __init__(self):
        self.unit_of_work: IUnitOfWork

    @abstractmethod
    async def add(self, entity: BaseModel):
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: BaseModel):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError


class Service(ServiceAbstract):
    base_repo: str

    def __init__(self):
        self.unit_of_work: UnitOfWork = UnitOfWork()

    async def add(self, entity):
        async with self.unit_of_work as ses:
            data = entity.model_dump()
            res = await ses.__dict__[self.base_repo].add_one(data)
            if res:
                return res
            raise HTTPException(status_code=404, detail=f"Not found {self.base_repo}")

    async def update(self, id, entity):
        async with self.unit_of_work as ses:
            data = entity.model_dump()
            res = await ses.__dict__[self.base_repo].edit_one(id, data)
            if res:
                return res
            raise HTTPException(status_code=404, detail=f"Not found {self.base_repo}")

    async def delete(self, id):
        async with self.unit_of_work as ses:
            res = await ses.__dict__[self.base_repo].delete_one(id)
            if res:
                return res
            raise HTTPException(status_code=404, detail=f"Not found {self.base_repo}")

    async def get(self, id):
        async with self.unit_of_work as ses:
            res = await ses.__dict__[self.base_repo].find_one(id=id)
            if res:
                return res

            raise HTTPException(status_code=404, detail=f"Not found {self.base_repo}")

    async def get_all(self):
        async with self.unit_of_work as ses:
            res = await ses.__dict__[self.base_repo].find_all()
            if res:
                return res
            raise HTTPException(status_code=504, detail=f"Not data")

    def set_session(self, uow):
        self.unit_of_work = uow
        return self
