from fastapi import APIRouter, Depends, Form
from typing import Annotated

from .services import SupplierService
from .entitys import SupplierResponse, SupplierScheme

router = APIRouter(tags=["supplier"], prefix="/supplier")

data = Annotated[SupplierScheme, Form()]


@router.post("/")
async def create_supplier(
    supplier: data, service: SupplierService = Depends(SupplierService)
):
    _id = await service.add_supplier(supplier)
    return {"id": _id}


@router.get("/all")
async def get_supplier(service: SupplierService = Depends(SupplierService)):
    return await service.get_suppliers()


@router.get("/{supplier}")
async def get_supplier(
    supplier: int, service: SupplierService = Depends(SupplierService)
):
    return await service.get_supplier(supplier)


@router.put("/{supplier}")
async def get_supplier(
    supplier: int,
    object: data,
    service: SupplierService = Depends(SupplierService),
):
    return await service.update_supplier(supplier, object)


@router.delete("/{supplier}")
async def get_supplier(
    supplier: int, service: SupplierService = Depends(SupplierService)
):
    return await service.delete_supplier(supplier)
