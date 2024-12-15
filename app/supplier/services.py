from fastapi import HTTPException


from .repository import SupplierDB
from .entitys import SupplierResponse, SupplierScheme


class SupplierService:
    def __init__(self):
        self.supplier_repositories = SupplierDB()
        self.model = SupplierResponse

    async def add_supplier(self, object):
        data = await self.supplier_repositories.add(object)
        if data:
            return data
        raise HTTPException(status_code=409, detail="Failed to add supplier")

    async def get_supplier(self, id: int):
        res = await self.supplier_repositories.get_by_id(id)
        if res:
            return self.model.model_validate(res)
        raise HTTPException(status_code=404, detail="supplier not found")

    async def update_supplier(self, id: int, object):
        data = await self.supplier_repositories.update_by_id(id, object)
        if data:
            return data
        raise HTTPException(status_code=404, detail="supplier not found")

    async def delete_supplier(self, id: int):
        data = await self.supplier_repositories.delete_by_id(id)
        if data:
            return data
        raise HTTPException(status_code=404, detail="supplier not found")

    async def get_suppliers(self):
        data = await self.supplier_repositories.get_all()
        if data:
            return [self.model.model_validate(_) for _ in data]
        raise HTTPException(status_code=504, detail="Data source is not available.")

    async def get_supplier_and_purchase(self, id):
        data = await self.supplier_repositories.get_by_id_where_purchase(id)
        if data:
            return data
        return False
