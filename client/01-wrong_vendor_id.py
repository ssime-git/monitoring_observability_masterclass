from httpx import Client, AsyncClient
import asyncio
import sys
import os
from utils import allowed_users
import pandas as pd
import random
import uuid

async def post_transaction(client, url, headers, transaction):
    response = await client.post(url, headers=headers, json=transaction, timeout=None)

def login(address, form_data):
    login_address = f"{address}/login/token"
    with Client() as client:
        response = client.post(login_address, data=form_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("Login successful!")
            return token
        else:
            print("Login failed:", response.json())
        
def get_transaction(series_products, product_indice):
    transaction = {}
    transaction["id"] = str(uuid.uuid4())
    transaction["product_id"] = series_products[product_indice]
    transaction["vendor_id"] = "02ebcce1-76d4-4eaf-8427-0c8dcf5dab27"
    transaction["action"] = "withdrawal"
    transaction["quantity"] = random.randint(1, 10)
    return transaction

async def test_post_transactions(fastapi_address, series_products, product_indice):
    tokens = []
    headers = {}
    url = f"{fastapi_address}/transactions"
    for i in range(len(allowed_users) - 20):
        tokens.append(login(fastapi_address, allowed_users[i]))
    headers['accept'] = 'application/json'
    async with AsyncClient() as ac:
        tasks = []
        for i in range(1, 1000):
            print(f"test {i} launched")
            await asyncio.sleep(random.uniform(4, 6))
            token_indice = random.randint(0, len(tokens) - 1)
            token = tokens[token_indice]
            headers['Authorization'] = f"Bearer {token}"
            transaction = get_transaction(series_products, product_indice)
            tasks.append(asyncio.ensure_future(post_transaction(ac, url,  headers, transaction)))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    fastapi_ip = sys.argv[1]
    port = os.environ.get("FASTAPI_PORT", "5000")
    fastapi_address = f"http://{fastapi_ip}:{port}"
    data_dir = "data"
    series_products = pd.read_csv(f"{data_dir}/products.csv", nrows=100)["id"]
    product_indice = random.randint(0, len(series_products) - 1)
    asyncio.run(test_post_transactions(fastapi_address, series_products, product_indice))
