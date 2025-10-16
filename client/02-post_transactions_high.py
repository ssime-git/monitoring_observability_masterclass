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
        
def get_transaction(series_vendors, series_products):
    transaction = {}
    transaction["id"] = str(uuid.uuid4())
    transaction["product_id"] = series_products[random.randint(0, len(series_products) - 1)]
    transaction["vendor_id"] = series_vendors[random.randint(0, len(series_vendors) - 1)]
    transaction["action"] = "withdrawal"
    transaction["quantity"] = random.randint(1, 10)
    return transaction

async def test_post_transactions(fastapi_address, series_vendors, series_products):
    tokens = []
    headers = {}
    url = f"{fastapi_address}/transactions"  # Changed back to /transactions to match the router prefix
    for i in range(len(allowed_users) - 20):
        tokens.append(login(fastapi_address, allowed_users[i]))
    headers['accept'] = 'application/json'
    async with AsyncClient() as ac:
        tasks = []
        for i in range(1, 10000):
            print(f"test {i} launched")
            await asyncio.sleep(20e-3)
            token_indice = random.randint(0, len(tokens) - 1)
            token = tokens[token_indice]
            headers['Authorization'] = f"Bearer {token}"
            transaction = get_transaction(series_vendors, series_products)
            tasks.append(asyncio.ensure_future(post_transaction(ac, url,  headers, transaction)))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    fastapi_ip = sys.argv[1]
    port = os.environ.get("FASTAPI_PORT", "5000")
    fastapi_address = f"http://{fastapi_ip}:{port}"
    
    # Load data
    data_dir = "data"
    series_vendors = pd.read_csv(f"{data_dir}/vendors.csv", nrows=100)["id"]
    series_products = pd.read_csv(f"{data_dir}/products.csv", nrows=100)["id"]
    
    asyncio.run(test_post_transactions(fastapi_address, series_vendors, series_products))
