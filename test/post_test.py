import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.run(order=1)
async def test_create_customer(client):

    response = await client.post(
        "/customer/",
        json={"name": "John Doe", "email": "test", "address": "street"},
    )

    assert response.status_code in range(200, 300)
    assert response.status_code == 201


async def test_create_supplier(client):

    response = await client.post(
        "/supplier/",
        json={"name": "Supplier A", "email": "test", "address": "street"},
    )
    assert response.status_code in range(200, 300)


async def test_create_supplier_error(client):

    response = await client.post(
        "/supplier/",
        json={"name": "Supplier A", "email": "test", "address": "street"},
    )

    assert response.status_code == 409
