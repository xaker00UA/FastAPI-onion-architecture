from fastapi import HTTPException
from app.product.repository import ProductDB
from .entitys import (
    PurchaseRequest,
    PurchaseResponse,
    PurchaseScheme,
    PartyRequest,
)
from .models import Purchases
from .repository import PurchasesDB, PartyDB
from ..product.services import ProductService
from ..supplier.services import SupplierService


class PurchaseService:
    def __init__(self) -> None:
        self.purchase_repo = PurchasesDB()
        self.party_repo = PartyDB()
        self.product_service = ProductService()
        self.supplier_service = SupplierService()
        self.model = PurchaseResponse

    async def add_purchase(self, purchase: PurchaseRequest) -> dict:
        # Получаем продукт
        product = await self.product_service.get_product(purchase.product_id)

        # Проверяем, есть ли уже активная покупка для данного поставщика
        supplier_purchase = await self.supplier_service.get_supplier_and_purchase(
            purchase.supplier_id
        )
        if not supplier_purchase.purchases:
            # Если у поставщика еще нет покупок, создаем новую
            new_purchase = PurchaseScheme(supplier_id=purchase.supplier_id)

            new_item = PartyRequest(
                product=product,
                quantity=purchase.quantity,
                product_id=product.id,
            )
            new_purchase.update_total(new_item.cost)
            # Сохраняем новую покупку и возвращаем данные
            saved_purchase = await self.purchase_repo.add(new_purchase)
            new_item.purchase_id = saved_purchase
            await self.party_repo.add(new_item)
            return saved_purchase

        else:
            saved_purchase = PurchaseScheme.model_validate(supplier_purchase.purchases)
            new_item = PartyRequest(
                product=product,
                quantity=purchase.quantity,
                product_id=product.id,
                purchase_id=supplier_purchase.purchases.id,
            )
            saved_purchase.update_total(new_item.cost)
            await self.party_repo.add(new_item)
            updated_purchase = await self.purchase_repo.update_by_id(
                supplier_purchase.purchases.id, saved_purchase
            )
            return updated_purchase

    async def get_purchase(self, _id: int):
        purchase = await self.purchase_repo.get_by_id(_id)
        if purchase:
            return self.model.model_validate(purchase)
        raise HTTPException(status_code=404, detail="purchase not found")
