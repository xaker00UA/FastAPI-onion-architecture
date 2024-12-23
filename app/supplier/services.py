from ..utils.service import Service
from .repository import SupplierRepository
from fastapi import HTTPException


class SupplierService(Service):
    base_repo = SupplierRepository.name_repo

    async def add(self, entity):
        async with self.unit_of_work as work:
            em = await work.__dict__[self.base_repo].is_email_unique(entity.email)
            if em:
                raise HTTPException(status_code=409, detail="email already exists")
        return await super().add(entity)
