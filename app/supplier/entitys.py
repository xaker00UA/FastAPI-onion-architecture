from pydantic import BaseModel


from ..customer.entitys import CustomerResponse, CustomerScheme


class SupplierScheme(CustomerScheme):
    pass


class SupplierResponse(CustomerResponse):
    pass
