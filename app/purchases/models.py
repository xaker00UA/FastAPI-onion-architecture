from datetime import datetime
from decimal import Decimal
from ..configurations.database import Base
from typing import Annotated
from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    DECIMAL,
    ForeignKey,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

# intpk = Annotated[BigInteger, mapped_column(primary_key=True)]
many = Annotated[DECIMAL, mapped_column(DECIMAL(10, 2))]


class Purchases(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    supplier_id: Mapped[BigInteger] = mapped_column(ForeignKey("suppliers.id"))
    total_amount: Mapped[many]

    items: Mapped[list["Party"]] = relationship(
        "Party", back_populates="purchase", lazy="joined"
    )
    supplier = relationship("Supplier", back_populates="purchases", lazy="joined")


class Party(Base):
    __tablename__ = "party"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"))
    purchase_id: Mapped[BigInteger] = mapped_column(ForeignKey("purchases.id"))
    quantity: Mapped[int] = mapped_column()
    cost: Mapped[many]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Пример использования при инициализации:
        if self.product:
            self.cost = self.quantity * self.product.price

    cost: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    purchase: Mapped["Purchases"] = relationship(back_populates="items")
    product = relationship(
        "Product", back_populates="parties", passive_deletes=True, lazy="joined"
    )
