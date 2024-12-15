from asyncpg import UniqueViolationError
from ..configurations.context_manager import get_db
from .models import Customer
from .entitys import CustomerScheme
from ..configurations.repository import BaseCrud


class CustomerDB(BaseCrud):
    model = Customer

    async def add(self, object):
        try:
            data = await super().add(object)
            return data
        except UniqueViolationError:
            return "unique email"
