from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, model_validator, computed_field

from ..supplier.entitys import SupplierResponse
from ..product.entitys import ProductResponse


class PurchaseRequest(BaseModel):
    supplier_id: int
    product_id: int
    quantity: int


class PurchaseScheme(BaseModel):
    supplier_id: int
    total_amount: Decimal = 0

    model_config = ConfigDict(from_attributes=True, extra="allow")

    def update_total(self, count):
        self.total_amount += count

    def calculate_total_amount(self, data: list):
        self.total_amount = 0
        for item in data:
            self.total_amount += item.price


class PartyRequest(BaseModel):
    product: ProductResponse
    quantity: int

    model_config = ConfigDict(extra="allow")

    @computed_field
    @property
    def cost(self) -> Decimal:
        """
        Вычисляет стоимость партии на основе цены продукта и количества.
        """
        if self.product.price is None:
            raise ValueError("Price of the product must be defined")
        return Decimal(self.product.price).quantize(Decimal("0.01")) * Decimal(
            self.quantity
        )


class PartyResponse(BaseModel):
    id: int
    product: ProductResponse
    created_at: datetime
    cost: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class PurchaseResponse(BaseModel):
    id: int
    total_amount: float
    supplier: SupplierResponse
    items: list[PartyResponse]

    model_config = ConfigDict(from_attributes=True)
