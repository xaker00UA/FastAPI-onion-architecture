from typing import Annotated
from fastapi import APIRouter, Depends
from .services import CustomerService
from ..utils.service import ServiceAbstract
from .entitys import CustomerScheme, CustomerResponse

router = APIRouter(prefix="/customer", tags=["customer"])


service = Annotated[ServiceAbstract, Depends(CustomerService)]


@router.get("/all", response_model=list[CustomerResponse])
async def get_all_customers(service: service):
    return await service.get_all()


@router.get("/{id}", response_model=CustomerResponse)
async def get_customer(id: int, service: service):
    return await service.get(id)


@router.post("/", status_code=201)
async def create_customer(data: CustomerScheme, service: service):
    return await service.add(data)


@router.put("/{id}")
async def update_customer(id: int, data: CustomerScheme, service: service):
    return await service.update(id, data)


@router.delete("/{id}", response_model=CustomerResponse)
async def delete_customer(id: int, service: service):
    return await service.delete(id)
