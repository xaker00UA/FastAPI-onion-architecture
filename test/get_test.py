import pytest


@pytest.mark.run(order=2)
async def test_get_customer(client):
    response = await client.get("/customer/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "John Doe"


async def test_get_supplier(client):
    response = await client.get("/supplier/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Supplier A"
