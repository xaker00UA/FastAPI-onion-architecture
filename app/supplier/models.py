from sqlalchemy.orm import relationship
from ..customer.models import CustomerAbstract
from .entitys import SupplierResponse


class Supplier(CustomerAbstract):
    __tablename__ = "suppliers"

    purchases = relationship("Purchases", back_populates="supplier", uselist=False)

    def to_read_model(self):
        return SupplierResponse.model_validate(self)
