from datetime import datetime

from ..purchases.entitys import PartyResponse
from ..configurations.db import Base
from typing import Annotated
from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    DECIMAL,
    ForeignKey,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entitys import SaleResponse

many = Annotated[DECIMAL, mapped_column(DECIMAL(10, 2))]


class Sales(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    customer_id: Mapped[BigInteger] = mapped_column(
        ForeignKey("customers.id", ondelete="SET NULL")
    )
    total_amount: Mapped[many]

    items: Mapped[list["Sales_Item"]] = relationship(
        "Sales_Item", back_populates="sale", lazy="joined"
    )
    customer = relationship("Customer", back_populates="sales", lazy="joined")

    def to_read_model(self):
        return SaleResponse.model_validate(self)


class Sales_Item(Base):
    __tablename__ = "sales_item"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"))
    sales_id: Mapped[int] = mapped_column(ForeignKey("sales.id"))
    quantity: Mapped[int] = mapped_column()
    cost: Mapped[many]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    sale = relationship("Sales", back_populates="items")
    product = relationship(
        "Product", backref="sales_item", passive_deletes=True, lazy="joined"
    )

    def to_read_model(self):
        return PartyResponse.model_validate(self)
