from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..customer.route import router as customer_router
from ..supplier.route import router as supplier_router
from ..product.route import router as product_router
from ..purchases.route import router as purchase_router
from ..sales.route import router as sales_router
from .db import drop_db, init_db

__router__ = (
    customer_router,
    product_router,
    supplier_router,
    purchase_router,
    sales_router,
)


class Server:

    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.register_routes(app)
        self.register_middlewares(app)
        # self.register_events(app)

    def get_app(self):
        return self.__app

    @staticmethod
    def register_events(app: FastAPI):
        @asynccontextmanager
        async def lifespan(app):
            await drop_db()
            await init_db()
            yield

        app.router.lifespan_context = lifespan

    @staticmethod
    def register_routes(app):
        for route in __router__:
            app.include_router(route)

    @staticmethod
    def register_middlewares(app):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
