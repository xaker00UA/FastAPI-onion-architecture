from typing import Any, Callable, Dict, List, Tuple
from fastapi.exceptions import HTTPException


from .repository import ProductDB
from .entitys import ProductResponse


class ErrorHandlingMixin:
    default_errors: Dict[int, Tuple[str, int]] = {
        "not_found": ("Resource not found", 404),
        "conflict": ("Conflict occurred", 409),
        "server_error": ("An unknown error occurred", 500),
    }

    async def safe_execute(
        self,
        method: Callable,
        *args: Any,
        error_cases: List[Tuple[str, int]] = None,
        default_error_key: str = "not_found",
        **kwargs: Any
    ):
        """
        Обёртка для вызова метода с обработкой ошибок.
        :param method: Метод, который вызывается.
        :param args: Аргументы метода.
        :param error_cases: Явно заданные ошибки (имеют приоритет).
        :param default_error_key: Ключ для стандартной ошибки (например, "not_found").
        :param kwargs: Именованные аргументы метода.
        :return: Результат метода, если он успешен.
        """
        result = await method(*args, **kwargs)
        if result:
            return result

        # Если есть явно заданные ошибки, обработать их
        if error_cases:
            for error_message, status_code in error_cases:
                raise HTTPException(status_code=status_code, detail=error_message)

        # Иначе использовать стандартную ошибку
        if default_error_key in self.default_errors:
            error_message, status_code = self.default_errors[default_error_key]
            raise HTTPException(status_code=status_code, detail=error_message)

        # Если даже стандартной ошибки нет, выбросить 500
        raise HTTPException(status_code=500, detail="An unknown error occurred")


# TODO: Написать универсальный класс миксин для ошибок
class ProductService(ErrorHandlingMixin):
    def __init__(self):
        self.product_repo = ProductDB()
        self.model = ProductResponse

    async def add_product(self, object):
        return await self.safe_execute(
            self.product_repo.add, object, error_cases=[("Failed to add product", 409)]
        )

    async def get_product(self, id: int):
        product = await self.safe_execute(
            self.product_repo.get_by_id,
            id,
            default_error_key="not_found",  # Использует стандартное "Resource not found"
        )
        return self.model.model_validate(product)

    async def update_product(self, id: int, object):
        return await self.safe_execute(
            self.product_repo.update_by_id,
            id,
            object,
            default_error_key="not_found",  # Использует стандартное "Resource not found"
        )

    async def delete_product(self, id: int):
        return await self.safe_execute(
            self.product_repo.delete_by_id,
            id,
            default_error_key="not_found",  # Использует стандартное "Resource not found"
        )

    async def get_products(self):
        products = await self.safe_execute(
            self.product_repo.get_all,
            error_cases=[("Data source is not available", 504)],
        )
        return [self.model.model_validate(product) for product in products]
