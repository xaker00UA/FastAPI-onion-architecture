import aiohttp
import asyncio
from random import randint
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="log.log",
    filemode="w",
    format="%(asctime)s |%(levelname)s| %(message)s",
)


async def create_sales(session):
    async with session.get(f"/product/{randint(1, 20)}") as response:
        product = await response.json()
        _id = product.get("id")
        if not _id:
            logging.error(product)
            return response.status
    async with session.get(f"/customer/{randint(1,1000)}") as response:
        customer = await response.json()
        customer_id = customer.get("id")
        if not customer_id:
            logging.error(str(customer))
            return response.status
    async with session.post(
        "/sales/",
        json={
            "product_id": _id,
            "customer_id": customer_id,
            "quantity": randint(1, 100),
        },
    ) as response:
        if response.status != 201:
            logging.error(await response.text())
        return response.status


async def create_party(session):
    async with session.get(f"/product/{randint(1, 20)}") as response:
        product = await response.json()
        _id = product.get("id")
        if not _id:
            logging.error(str(product))
            return response.status
    async with session.get(f"/supplier/{randint(1,1000)}") as response:
        supplier = await response.json()
        supplier_id = supplier.get("id")
        if not supplier_id:
            logging.error(str(supplier))
            return response.status
    async with session.post(
        "/purchases/",
        json={
            "product_id": _id,
            "supplier_id": supplier_id,
            "quantity": randint(1, 20) * 50,
        },
    ) as response:
        if response.status != 201:
            logging.error(await response.text())
        return response.status


async def main():
    async with aiohttp.ClientSession(base_url="http://localhost:3000") as session:
        task = []
        result = []
        # task.extend([asyncio.create_task(create_party(session)) for _ in range(9990)])
        # done, pen = await asyncio.wait(task)
        # result.extend(done)
        # task = []
        task.extend([asyncio.create_task(create_sales(session)) for _ in range(10000)])
        done, pen = await asyncio.wait(task)
        result.extend(done)
    for res in done:
        res = res.result()
        if res != 201:
            if res >= 500:
                print(res)
                break
            print(res)


if __name__ == "__main__":
    asyncio.run(main())
