from sqlalchemy import delete, select
from ..utils.repositorie import SQLAlchemyRepository
from .models import Sales, Sales_Item


class SalesRepository(SQLAlchemyRepository):
    model = Sales
    name_repo = "sales"


class SalesItemRepository(SQLAlchemyRepository):
    model = Sales_Item
    name_repo = "sales_item"

    async def delete_one(self, id: int) -> int:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def find_all_where_filter(self, **kwargs):
        stmt = select(self.model).filter(**kwargs)
        res = await self.session.execute(stmt)
        return [row[0].to_read_model() for row in res.unique().all()]
