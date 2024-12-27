from sqlalchemy import select
from ..utils.repositorie import SQLAlchemyRepository
from .models import Supplier


class SupplierRepository(SQLAlchemyRepository):
    model = Supplier
    name_repo = "supplier"

    async def is_email_unique(self, email: str) -> bool:
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
