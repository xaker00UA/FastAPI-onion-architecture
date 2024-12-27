from ..utils.repositorie import SQLAlchemyRepository
from .models import Product


class ProductRepository(SQLAlchemyRepository):
    model = Product
    name_repo = "product"
