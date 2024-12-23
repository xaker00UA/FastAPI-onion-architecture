import aiohttp
import asyncio


async def random_user():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://randomuser.me/api/") as response:
            i = 0
            exciton = None
            while i < 100:
                if response.status != 200:
                    i += 1
                    exciton = await response.text()
                    await asyncio.sleep(1)
                    continue
                else:
                    data = await response.json()
                    name = data["results"][0]["name"]["first"]
                    email = data["results"][0]["email"]
                    location = data["results"][0]["location"]
                    address = (
                        location["country"]
                        + " "
                        + location["state"]
                        + " "
                        + location["city"]
                        + " "
                        + location["street"]["name"]
                        + " "
                        + str(location["street"]["number"])
                    )
                    return {"name": name, "email": email, "address": address}
            raise Exception("api error: %s" % exciton)


async def random_product():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://fakestoreapi.com/products") as response:
            res = await response.json()
            data = []
            for i in res:
                data.append(
                    {
                        "name": i["title"],
                        "price": float(i["price"]),
                        "description": i["description"],
                    }
                )
            return data


async def post(semaphore, session: aiohttp.ClientSession, url: str):
    async with semaphore:
        data = await random_user()
        async with session.post(url, json=data) as response:
            return await response.json()


async def add_product():
    data = await random_product()
    async with aiohttp.ClientSession(base_url="http://localhost:3000") as session:
        for i in data:
            async with session.post("/product/", json=i) as response:
                await response.json()

        return


async def main():
    semaphore = asyncio.Semaphore(5)
    async with aiohttp.ClientSession(base_url="http://localhost:3000") as session:
        # Создаём список задач
        tasks = []
        # tasks.append(asyncio.create_task(add_product()))
        # tasks.extend(
        #     [
        #         asyncio.create_task(post(semaphore, session, "/customer/"))
        #         for _ in range(3)
        #     ]
        # )
        tasks.extend(
            [
                asyncio.create_task(post(semaphore, session, "/supplier/"))
                for _ in range(1)
            ]
        )

        # Запускаем все задачи одновременно и ждём их выполнения
        done, pending = await asyncio.wait(tasks)

        # Обрабатываем результаты
        for task in done:
            result = task.exception()
            if result:  # Получаем результат выполнения задачи
                print(result)


if __name__ == "__main__":
    asyncio.run(main())
