from typing import Annotated

from fastapi import APIRouter, Depends

from .services import SalesService, SaleItemService
from ..utils.service import ServiceAbstract
from .entitys import SaleScheme, PartyResponse, SaleResponse

router = APIRouter(tags=["sales"], prefix="/sales")
service = Annotated[SalesService, Depends(SalesService)]
party = Annotated[ServiceAbstract, Depends(SaleItemService)]


@router.get("/all", response_model=list[PartyResponse])
async def get_all_party(service: party):
    return await service.get_all()


@router.get("/{id}", response_model=PartyResponse)
async def get_party(id: int, service: party):
    return await service.get(id)


@router.get("/all/sales", response_model=list[SaleResponse])
async def get_all_purchases(service: service):
    return await service.get_all()


@router.get("/", response_model=SaleResponse)
async def get_purchase_supplier(customer_id: int, service: service):
    return await service.get_supplier(customer_id)


@router.post("/", status_code=201)
async def create_purchase(purchase: SaleScheme, service: service) -> int:
    return await service.add(purchase)


@router.delete("/{id}")
async def delete_purchase(id: int, service: service) -> PartyResponse:
    return await service.delete(id)
