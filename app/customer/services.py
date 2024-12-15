from fastapi.exceptions import HTTPException


from .repository import CustomerDB
from .entitys import CustomerResponse
from ..configurations.context_manager import get_db


# TODO: Написать универсальный класс миксин для ошибок
class CustomerService:
    def __init__(self):
        self.customer_repositories = CustomerDB()
        self.model = CustomerResponse

    async def add_customer(self, object):
        data = await self.customer_repositories.add(object)
        if data:
            return data
        raise HTTPException(status_code=409, detail="Failed to add customer")

    async def get_customer(self, id: int):
        res = await self.customer_repositories.get_by_id(id)
        if res:
            return self.model.model_validate(res)
        raise HTTPException(status_code=404, detail="Customer not found")

    async def update_customer(self, id: int, object):
        data = await self.customer_repositories.update_by_id(id, object)
        if data:
            return data
        raise HTTPException(status_code=404, detail="Customer not found")

    async def delete_customer(self, id: int):
        data = await self.customer_repositories.delete_by_id(id)
        if data:
            return data
        raise HTTPException(status_code=404, detail="Customer not found")

    async def get_customers(self):
        data = await self.customer_repositories.get_all()
        if data:
            return [self.model.model_validate(_) for _ in data]
        raise HTTPException(status_code=504, detail="Data source is not available.")
