from typing import Annotated

from fastapi import APIRouter, Depends

from .services import PurchasesService, PartyService
from ..utils.service import ServiceAbstract
from .entitys import PurchaseScheme, PartyResponse, PurchaseResponse

router = APIRouter(tags=["purchases"], prefix="/purchases")
service = Annotated[PurchasesService, Depends(PurchasesService)]
party = Annotated[ServiceAbstract, Depends(PartyService)]


@router.get("/all", response_model=list[PartyResponse])
async def get_all_party(service: party):
    return await service.get_all()


@router.get("/{id}", response_model=PartyResponse)
async def get_party(id: int, service: party):
    return await service.get(id)


@router.get("/all/purchases", response_model=list[PurchaseResponse])
async def get_all_purchases(service: service):
    return await service.get_all()


@router.get("/", response_model=PurchaseResponse)
async def get_purchase_supplier(supplier_id: int, service: service):
    return await service.get_supplier(supplier_id)


@router.post("/", status_code=201)
async def create_purchase(purchase: PurchaseScheme, service: service) -> int:
    return await service.add(purchase)


@router.delete("/{id}", response_model=PartyResponse)
async def delete_purchase(id: int, service: service):
    return await service.delete(id)
