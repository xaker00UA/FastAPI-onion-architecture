from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from .services import SupplierService
from ..utils.service import ServiceAbstract
from .entitys import CustomerScheme, CustomerResponse

router = APIRouter(prefix="/supplier", tags=["supplier"])


service = Annotated[ServiceAbstract, Depends(SupplierService)]


@router.get("/all", status_code=200, response_model=list[CustomerResponse])
async def get_all_customers(service: service):
    return await service.get_all()


@router.get("/{id}", status_code=200, response_model=CustomerResponse)
async def get_customer(id: int, service: service):
    return await service.get(id)


@router.post("/", status_code=201)
async def create_customer(data: CustomerScheme, service: service):
    return await service.add(data)


@router.put("/{id}", status_code=200)
async def update_customer(id: int, data: CustomerScheme, service: service):
    return await service.update(id, data)


@router.delete("/{id}", status_code=200, response_model=CustomerResponse)
async def delete_customer(id: int, service: service):
    return await service.delete(id)
