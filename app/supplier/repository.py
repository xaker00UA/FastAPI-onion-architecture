from sqlalchemy import select
from sqlalchemy.orm import joinedload
from .models import Supplier
from ..customer.repository import CustomerDB


class SupplierDB(CustomerDB):
    model: Supplier = Supplier

    async def get_by_id_where_purchase(self, id: int) -> Supplier | None:
        async with self.get_session() as ses:
            result = await ses.execute(
                select(self.model)
                .options(
                    joinedload(self.model.purchases)
                )  # Подгружаем связанные покупки
                .filter(self.model.id == id)  # Фильтруем по id
            )
            return (
                result.scalars().first()
            )  # Возвращаем первую найденную запись или None
