from ..customer.models import CustomerAbstract
from sqlalchemy.orm import relationship


class Supplier(CustomerAbstract):
    __tablename__ = "suppliers"

    purchases = relationship("Purchases", back_populates="supplier", uselist=False)
