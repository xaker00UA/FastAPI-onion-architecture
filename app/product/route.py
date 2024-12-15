from fastapi import APIRouter, Depends
from fastapi import Form
from typing import Annotated
from .entitys import ProductScheme
from .services import ProductService

router = APIRouter(tags=["product"], prefix="/product")
party = APIRouter(tags=["party"], prefix="/party")


@router.post("/")
async def create_product(
    product: ProductScheme, service: ProductService = Depends(ProductService)
):
    _id = await service.add_product(product)
    return {"id": _id}


@router.get("/all")
async def get_product(service: ProductService = Depends(ProductService)):
    return await service.get_products()


@router.get("/{product}")
async def get_product(product: int, service: ProductService = Depends(ProductService)):
    return await service.get_product(product)


@router.delete("/{product}")
async def get_product(product: int, service: ProductService = Depends(ProductService)):
    return await service.delete_product(product)


@router.put("/{product}")
async def get_product(
    product: int,
    object: ProductScheme,
    service: ProductService = Depends(ProductService),
):
    return await service.update_product(product, object)
