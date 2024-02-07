import aiohttp
import asyncio

# Тут будет логика для поиска оптимального кошелька.

async def fetch_account_info():
    url = "https://api.shasta.trongrid.io/wallet/getaccount"
    payload = {
        "address": "TEq7EykArxp8kuZJ6uQK6u2u97MN5tDqHB",
        "visible": True
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            return await response.text()

async def main():
    response_text = await fetch_account_info()
    print(response_text)

if __name__ == "__main__":
    asyncio.run(main())
