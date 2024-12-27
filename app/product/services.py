from ..utils.service import Service
from .repository import ProductRepository


class ProductService(Service):
    base_repo = ProductRepository.name_repo
