from datetime import datetime
from decimal import Decimal
from pydantic import (
    BaseModel,
    ConfigDict,
    model_serializer,
    computed_field,
)

from ..customer.entitys import CustomerResponse
from ..product.entitys import ProductResponse
from ..purchases.entitys import PartyResponse


class SaleScheme(BaseModel):
    customer_id: int
    product_id: int
    quantity: int


class SaleRequest(SaleScheme):
    total_amount: Decimal = 0

    model_config = ConfigDict(from_attributes=True)

    @model_serializer()
    def serialize_model(self):
        return {
            "total_amount": self.total_amount,
            "customer_id": self.customer_id,
        }

    def update_total(self, count):
        self.total_amount += count

    def calculate_total_amount(self, data: list):
        self.total_amount = 0
        for item in data:
            self.total_amount += item.price


class SalesItemRequest(SaleScheme):
    product: ProductResponse
    quantity: int

    sale_id: int = -1

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def cost(self) -> float:
        return self.product.price * self.quantity

    @model_serializer()
    def serialize_model(self):
        return {
            "product_id": self.product.id,
            "quantity": self.quantity,
            "cost": self.cost,
            "sales_id": self.sale_id,
        }


class SaleResponse(BaseModel):
    id: int
    total_amount: float
    customer: CustomerResponse
    items: list["PartyResponse"] | None

    model_config = ConfigDict(from_attributes=True)

    def update_total(self, count):
        self.total_amount += count

    def calculate_total_amount(
        self,
    ):
        self.total_amount = 0
        for item in self.items:
            self.total_amount += item.cost
