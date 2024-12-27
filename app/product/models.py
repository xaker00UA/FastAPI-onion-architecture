from decimal import Decimal
from sqlalchemy import String, BigInteger, DECIMAL, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..configurations.db import Base
from .entitys import ProductResponse


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(250))
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    description: Mapped[str] = mapped_column(TEXT, nullable=True)

    parties = relationship(
        "Party", back_populates="product", cascade="all, delete-orphan"
    )

    def to_read_model(self):
        return ProductResponse.model_validate(self)
