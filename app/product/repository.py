from asyncpg import UniqueViolationError
from ..configurations.context_manager import get_db
from .models import Product
from .entitys import ProductScheme
from ..configurations.repository import BaseCrud


class ProductDB(BaseCrud):
    model = Product
