from sqlalchemy import select
from ..utils.repositorie import SQLAlchemyRepository
from .models import Customer


class CustomerRepository(SQLAlchemyRepository):
    model = Customer
    name_repo = "customer"

    async def is_email_unique(self, email: str) -> bool:
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
