from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .entitys import CustomerResponse
from ..configurations.db import Base


class CustomerAbstract(Base):

    __abstract__ = True

    id: Mapped[BigInteger] = mapped_column(BigInteger(), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    address: Mapped[str] = mapped_column(String(200), nullable=True)


class Customer(CustomerAbstract):
    __tablename__ = "customers"

    sales = relationship("Sales", back_populates="customer")

    def to_read_model(self):
        return CustomerResponse.model_validate(self.__dict__)
