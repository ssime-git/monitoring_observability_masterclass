from httpx import Client, AsyncClient
import asyncio
import sys
import os
from utils import allowed_users
import pandas as pd
import random
import uuid

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

async def resupply_products(client, url, headers):
    response = await client.put(url, headers=headers, timeout=None)
    if response.status_code == 200:
        print("Products resupplied successfully!")
    else:
        print("Failed to resupply products:", response.json())

async def test_resupply(address):
    token = login(address, allowed_users[0])
    url = f"{address}/products/quantity"
    
    async with AsyncClient() as client:
        while True:
            headers = {"Authorization": f"Bearer {token}"}
            await resupply_products(client, url, headers)
            await asyncio.sleep(30)  # Sleep for 30 seconds

if __name__ == "__main__":
    fastapi_ip = sys.argv[1]
    port = os.environ.get("FASTAPI_PORT", "5000")
    fastapi_address = f"http://{fastapi_ip}:{port}"
    
    asyncio.run(test_resupply(fastapi_address))
