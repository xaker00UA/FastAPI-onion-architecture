from fastapi import HTTPException
from ..utils.service import Service
from .repository import PurchasesRepository, PartyRepository
from .entitys import (
    PurchaseScheme,
    PartyRequest,
    PurchaseRequest,
    PurchaseResponse,
    PartyResponse,
)

from ..product.services import ProductService
from ..supplier.services import SupplierService


class PurchasesService(Service):
    base_repo = PurchasesRepository.name_repo

    def __init__(self):
        super().__init__()
        self.product_service = ProductService()
        self.supplier_service = SupplierService()
        self.party_service = PartyService()

    async def get_supplier(self, supplier_id) -> PurchaseResponse | None:
        async with self.unit_of_work as work:
            return await work.__dict__[self.base_repo].find_one(supplier_id=supplier_id)

    async def add(self, entity: PurchaseScheme):
        product = await self.product_service.get(entity.product_id)
        supplier = await self.supplier_service.get(entity.supplier_id)
        party = PartyRequest.model_validate({**entity.model_dump(), "product": product})

        old_purchase = await self.get_supplier(supplier.id)
        purchase_data = entity.model_dump()
        async with self.unit_of_work as work:
            if old_purchase:
                old_purchase.update_total(party.cost)
                party.purchase_id = old_purchase.id
                purchase_data["total_amount"] = old_purchase.total_amount
                await self.update(old_purchase.id, PurchaseRequest(**purchase_data))
            else:
                purchase = PurchaseRequest.model_validate(entity)
                purchase.update_total(party.cost)
                result = await super().add(purchase)
                party.purchase_id = result.get("id")
            self.party_service.set_session(work)
            return await self.party_service.add(party)

    async def delete(self, id):
        async with self.unit_of_work as work:
            self.party_service.set_session(work)
            party = await self.party_service.delete(id)
            purchase = await self.get(id=party.purchase_id)
            purchase.calculate_total_amount()
            data = PurchaseRequest(
                supplier_id=purchase.supplier.id,
                product_id=party.product_id,
                quantity=party.quantity,
                total_amount=purchase.total_amount,
            )
            await super().set_session(work).update(purchase.id, data)
            return party


class PartyService(Service):
    base_repo = PartyRepository.name_repo

    async def get_all_where_product(self, product_id) -> list[PartyResponse] | None:
        async with self.unit_of_work as work:
            res = await work.__dict__[self.base_repo].find_all_where_filter(product_id)
            if res:
                return res
            raise HTTPException(status_code=404, detail="Not Found party product")
