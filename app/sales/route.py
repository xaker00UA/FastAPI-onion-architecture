from typing import Annotated

from fastapi import APIRouter, Depends

from .services import SalesService, SaleItemService
from ..utils.service import ServiceAbstract
from .entitys import SaleScheme

router = APIRouter(tags=["sales"], prefix="/sales")
service = Annotated[SalesService, Depends(SalesService)]
party = Annotated[ServiceAbstract, Depends(SaleItemService)]


@router.get("/all")
async def get_all_party(service: party):
    return await service.get_all()


@router.get("/{id}")
async def get_party(id: int, service: party):
    return await service.get(id)


@router.get("/all/sales")
async def get_all_purchases(service: service):
    return await service.get_all()


@router.get("/")
async def get_purchase_supplier(customer_id: int, service: service):
    return await service.get_supplier(customer_id)


@router.post("/", status_code=201)
async def create_purchase(purchase: SaleScheme, service: service):
    return await service.add(purchase)


@router.delete("/{id}")
async def delete_purchase(id: int, service: service):
    return await service.delete(id)
