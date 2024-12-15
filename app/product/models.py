from datetime import datetime
from decimal import Decimal
from ..configurations.database import Base

from sqlalchemy import (
    TIMESTAMP,
    String,
    BigInteger,
    DECIMAL,
    Text,
    ForeignKey,
    text,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    description: Mapped[str] = mapped_column(Text, nullable=True)

    parties = relationship(
        "Party", back_populates="product", cascade="all, delete-orphan"
    )
