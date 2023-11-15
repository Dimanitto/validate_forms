import asyncio
from httpx import AsyncClient


async def make_requests():
    async with AsyncClient() as client:
        # Тест 1
        response = await client.post("http://localhost:8000/get_form", json={'email': "test@ya.ru"})
        data = response.json()
        print("Test 1:")
        print(data)
        print("Status Code:", response.status_code)
        print()

        # Тест 2
        response = await client.post("http://localhost:8000/get_form", json={
            "lead_email": "tester@ya.ru",
            "user_phone": '+7 999 888 77 66'
        })
        data = response.json()
        print("Test 2:")
        print(data)
        print("Status Code:", response.status_code)

        # Тест 3
        response = await client.post(
            "http://localhost:8000/get_form",
            json={
                "f_name11": "15.11.2023",
                "f_name22": 'text'
            },
        )
        data = response.json()
        print("Test 3:")
        print(data)
        print("Status Code:", response.status_code)


if __name__ == "__main__":
    asyncio.run(make_requests())
