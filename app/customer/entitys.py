from pydantic import BaseModel, ConfigDict, field_validator


class CustomerScheme(BaseModel):

    name: str
    email: str | None = None
    address: str | None = None

    @field_validator("email", mode="before")
    def empty_email_to_none(cls, v):
        if v == "":
            return None
        return v

    @field_validator("address", mode="before")
    def empty_address_to_none(cls, v):
        if v == "":
            return None
        return v

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        # Перемещаем `id` в начало, если оно существует
        if "id" in data:
            return {"id": data.pop("id"), **data}
        return data


class CustomerResponse(CustomerScheme):
    id: int

    model_config = ConfigDict(from_attributes=True)
