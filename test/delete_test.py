import pytest


@pytest.mark.run(order=5)
async def test_product_delete_error(client):
    response = await client.delete("/products/1")
    assert response.status_code == 404


async def test_supplier_delete(client):
    response = await client.delete("/supplier/1")
    assert response.status_code == 200
