from fastapi import HTTPException
from time import time
from ..utils.service import Service
from .repository import SalesItemRepository, SalesRepository
from .entitys import (
    SaleScheme,
    SalesItemRequest,
    SaleRequest,
    SaleResponse,
    PartyResponse,
)

from ..product.services import ProductService
from ..customer.services import CustomerService
from ..purchases.services import PartyService


class SalesService(Service):
    base_repo = SalesRepository.name_repo

    def __init__(self):
        super().__init__()
        self.product_service = ProductService()
        self.sales_item_service = SaleItemService()
        self.customer_service = CustomerService()
        self.party_service = PartyService()

    async def get_customer(self, customer_id) -> SaleResponse | None:
        async with self.unit_of_work as work:
            return await work.__dict__[self.base_repo].find_one(customer_id=customer_id)

    async def add(self, entity: SaleScheme):
        product = await self.product_service.get(entity.product_id)
        customer = await self.customer_service.get(entity.customer_id)
        parts = await self.party_service.get_all_where_product(product_id=product.id)
        item = SalesItemRequest.model_validate(
            {**entity.model_dump(), "product": product}
        )

        # Обновление количества товара в партиях
        quantity = await self.update_party_quantities(parts, item.quantity)
        if quantity > 0:
            raise HTTPException(
                status_code=409, detail="there is no such quantity of goods"
            )

        old_sale = await self.get_customer(customer.id)
        sale = self.prepare_sale(entity, old_sale, item).model_dump()

        async with self.unit_of_work as work:
            st = time()
            repo_party = work.get_repository("party")
            repo_sales = work.get_repository("sales")
            repo_item = work.get_repository("sales_item")

            # Обновление/создание продажи
            if old_sale:
                await repo_sales.edit_one(old_sale.id, sale)
            else:
                res = await repo_sales.add_one(sale)
                item.sale_id = res.get("id")  # Получаем ID для новой продажи

            # Обновление партий
            await self.update_parties_list(parts, repo_party)

            # Добавление записи в продажах
            res = await repo_item.add_one(item.model_dump())
            print(time() - st)
            return res

    async def delete(self, id):
        async with self.unit_of_work as work:
            self.party_service.set_session(work)
            party_response = await self.sales_item_service.get(id)
            party = await self.sales_item_service.delete(id)
            sales = await self.get(id=party.sales_id)
            sales.calculate_total_amount()
            data = SaleRequest(
                customer_id=sales.customer.id,
                product_id=party.product_id,
                quantity=party.quantity,
                total_amount=sales.total_amount,
            )
            await self.update(sales.id, data)
            return party_response

    async def update_party_quantities(self, parts, required_quantity):
        """Обновляем количество товара в партиях."""
        for part in parts:
            if part.quantity >= required_quantity:
                part.quantity -= required_quantity
                required_quantity = 0
                break
            else:
                required_quantity -= part.quantity
                part.quantity = 0
        return required_quantity

    def prepare_sale(self, entity: SaleScheme, old_sale, item):
        """Подготовка данных о продаже, обновление стоимости."""
        if old_sale:
            old_sale.update_total(item.cost)
            item.sale_id = old_sale.id
            return SaleRequest(
                customer_id=entity.customer_id,
                total_amount=old_sale.total_amount,
                product_id=entity.product_id,
                quantity=item.quantity,
            )
        else:
            sale = SaleRequest.model_validate(entity)
            sale.update_total(item.cost)
            return sale

    async def update_parties_list(self, parts, repo_party):
        """Обновление партий товара с использованием bulk_update_mappings."""
        updates = [{"id": part.id, "quantity": part.quantity} for part in parts]

        await repo_party.update_list(updates)


class SaleItemService(Service):
    base_repo = SalesItemRepository.name_repo
