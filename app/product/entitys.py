from pydantic import BaseModel, ConfigDict


class ProductScheme(BaseModel):

    name: str
    price: float
    description: str | None = None

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        # Перемещаем `id` в начало, если оно существует
        if "id" in data:
            return {"id": data.pop("id"), **data}
        return data


class ProductResponse(ProductScheme):
    id: int

    model_config = ConfigDict(from_attributes=True)
