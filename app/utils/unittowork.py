from abc import ABC, abstractmethod
from types import TracebackType
from typing import Type, TypedDict

from .repositorie import SQLAlchemyRepository
from ..configurations.context_manager import SessionLocal


from ..customer.repository import CustomerRepository
from ..supplier.repository import SupplierRepository
from ..product.repository import ProductRepository
from ..purchases.repository import PurchasesRepository, PartyRepository
from ..sales.repository import SalesRepository, SalesItemRepository

__repositories__ = (
    CustomerRepository,
    SupplierRepository,
    ProductRepository,
    PurchasesRepository,
    PartyRepository,
)


# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = SessionLocal
        self.repositories = {}
        self.__session = None
        self.__count_opens = 0
        self.__errors = []

    async def __aenter__(self):
        if not self.__session:
            self.__session = self.session_factory()
            self._register_repositories()

        self.__count_opens += 1
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.__count_opens -= 1
        if exc_type:
            await self.rollback()
            self.__errors.append(exc_val)
        if self.__count_opens == 0:
            if not self.__errors:
                await self.commit()
            else:
                await self.rollback()
            await self.__session.close()

    async def commit(self):
        await self.__session.commit()

    async def rollback(self):
        await self.__session.rollback()

    def _register_repositories(self):

        for repo_cls in SQLAlchemyRepository.__subclasses__():
            repo_name = repo_cls.name_repo
            obj = repo_cls(self.session)
            self.repositories[repo_name] = obj
            setattr(self, repo_name, obj)

    def get_repository(self, repo_name: str) -> SQLAlchemyRepository:
        return self.repositories[repo_name]

    @property
    def session(self):
        return self.__session
