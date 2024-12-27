from typing import Annotated
from fastapi import APIRouter, Depends
from .services import ProductService
from ..utils.service import ServiceAbstract
from .entitys import ProductScheme, ProductResponse

router = APIRouter(tags=["product"], prefix="/product")

service = Annotated[ServiceAbstract, Depends(ProductService)]


@router.post("/", status_code=201)
async def create_product(product: ProductScheme, service: service):
    return await service.add(product)


@router.get("/all", response_model=list[ProductResponse])
async def get_product(service: service):
    return await service.get_all()


@router.get("/{id}", response_model=ProductResponse)
async def get_product(id: int, service: service):
    return await service.get(id)


@router.delete("/{id}", response_model=ProductResponse)
async def get_product(id: int, service: service):
    return await service.delete(id)


@router.put("/{id}")
async def get_product(id: int, product: ProductScheme, service: service):
    return await service.update(id, product)
