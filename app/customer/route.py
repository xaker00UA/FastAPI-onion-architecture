from fastapi import APIRouter, Depends, Request
from .services import CustomerService
from .entitys import CustomerScheme

router = APIRouter(tags=["customer"], prefix="/customer")


@router.post("/")
async def create_customer(
    customer: CustomerScheme, service: CustomerService = Depends(CustomerService)
):
    _id = await service.add_customer(customer)
    return {"id": _id}


@router.get("/all")
async def get_customer(service: CustomerService = Depends(CustomerService)):
    return await service.get_customers()


@router.get("/{customer}")
async def get_customer(
    customer: int, service: CustomerService = Depends(CustomerService)
):
    return await service.get_customer(customer)


@router.delete("/{customer}")
async def get_customer(
    customer: int, service: CustomerService = Depends(CustomerService)
):
    return await service.delete_customer(customer)


@router.put("/{customer}")
async def get_customer(
    customer: int,
    object: CustomerScheme,
    service: CustomerService = Depends(CustomerService),
):
    return await service.update_customer(customer, object)
