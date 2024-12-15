from fastapi import APIRouter, Depends, Form
from typing import Annotated

from .entitys import PurchaseScheme, PurchaseRequest
from .services import PurchaseService

router = APIRouter(tags=["purchases"], prefix="/purchases")

data = Annotated[PurchaseRequest, Form()]


@router.get("/")
async def get_all_purchases(
    purchase_id: int, service: PurchaseService = Depends(PurchaseService)
):
    return await service.get_purchase(purchase_id)


@router.post("/")
async def create_purchase(
    purchase: data, service: PurchaseService = Depends(PurchaseService)
):
    return await service.add_purchase(purchase)


@router.delete("/{object}")
async def delete_purchase(object: int):
    pass


@router.get("/{object}")
async def get_purchase(
    object: int, service: PurchaseService = Depends(PurchaseService)
):
    pass
