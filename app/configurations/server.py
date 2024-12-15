from fastapi import FastAPI, APIRouter
from app.customer.route import router as customer_router
from app.product.route import router as product_router, party as party_route
from app.supplier.route import router as supplier_router
from app.purchases.route import router as purchase_router

root = APIRouter()


@root.get("/")
async def index():
    return {"message": "Welcome to the Inventory Management System"}


__router__ = (
    root,
    customer_router,
    product_router,
    party_route,
    supplier_router,
    purchase_router,
)


class Server:

    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.register_routes(app)

    def get_app(self):
        return self.__app

    @staticmethod
    def register_events(): ...

    @staticmethod
    def register_routes(app):
        for route in __router__:
            app.include_router(route)
