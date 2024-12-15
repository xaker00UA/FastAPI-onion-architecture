from asyncpg import UniqueViolationError
from sqlalchemy import select
from .models import Purchases, Party

from ..configurations.repository import BaseCrud


class PurchasesDB(BaseCrud):
    model: Purchases = Purchases


class PartyDB(BaseCrud):
    model = Party

    async def get_product_by_id(self, product_id, purchase_id) -> Party | None:
        async with self.get_session() as ses:
            result = await ses.execute(
                select(self.model).filter(
                    self.model.product_id == product_id
                    and self.model.purchase_id == purchase_id
                )
            )
            return result.scalars().first()
