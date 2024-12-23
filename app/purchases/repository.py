from sqlalchemy import bindparam, delete, select, desc, update
from ..utils.repositorie import SQLAlchemyRepository
from .models import Purchases, Party


class PurchasesRepository(SQLAlchemyRepository):
    model = Purchases
    name_repo = "purchases"


class PartyRepository(SQLAlchemyRepository):
    model = Party
    name_repo = "party"

    async def delete_one(self, id: int) -> int:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def find_all_where_filter(self, product_id: int) -> list[Party]:
        stmt = (
            select(self.model)
            .filter(self.model.product_id == product_id, self.model.quantity != 0)
            .order_by(self.model.created_at)
        )
        res = await self.session.execute(stmt)
        return [row.to_read_model() for row in res.scalars().all()]

    async def update_list(self, list_update: list):
        await self.session.execute(
            update(self.model).execution_options(synchronize_session=None), list_update
        )
