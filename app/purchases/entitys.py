from datetime import datetime
from decimal import Decimal
from pydantic import (
    BaseModel,
    ConfigDict,
    model_serializer,
    model_validator,
    computed_field,
)

from ..supplier.entitys import SupplierResponse
from ..product.entitys import ProductResponse


class PurchaseScheme(BaseModel):
    supplier_id: int
    product_id: int
    quantity: int


class PurchaseRequest(PurchaseScheme):
    total_amount: Decimal = 0

    model_config = ConfigDict(from_attributes=True)

    @model_serializer()
    def serialize_model(self):
        return {
            "total_amount": self.total_amount,
            "supplier_id": self.supplier_id,
        }

    def update_total(self, count):
        self.total_amount += count

    def calculate_total_amount(self, data: list):
        self.total_amount = 0
        for item in data:
            self.total_amount += item.price


class PartyRequest(PurchaseScheme):
    product: ProductResponse
    quantity: int

    purchase_id: int = -1

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
            "purchase_id": self.purchase_id,
        }


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
    items: list[PartyResponse] | None

    model_config = ConfigDict(from_attributes=True)

    def update_total(self, count):
        self.total_amount += count

    def calculate_total_amount(
        self,
    ):
        self.total_amount = 0
        for item in self.items:
            self.total_amount += item.cost
