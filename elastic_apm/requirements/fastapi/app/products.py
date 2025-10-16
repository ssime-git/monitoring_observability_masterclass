from fastapi import APIRouter, Depends
from login import manager
from logger import logger
import time
from postgres import connect_psql
import random
import uuid

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("")
async def get(user=Depends(manager)):
    with connect_psql() as conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM products''')
            result = cursor.fetchall()
            conn.commit()
            return result
        except Exception as exception:
            if cursor is not None:
                cursor.execute("ROLLBACK")
            logger.error(exception)
        finally:
            if cursor is not None:
                cursor.close()

def get_transactions(rows, id, vendor_id):
    transactions = []
    for row in rows:
        product_id = row[0]
        transaction = (id, product_id, vendor_id, "addition", 50)
        transactions.append(transaction)
    return transactions

@router.put("/quantity")
async def put_quantity(user=Depends(manager)):
    with connect_psql() as conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products
                SET quantity = quantity + 50
                WHERE quantity < 50
                RETURNING id
            ''')
            rows = cursor.fetchall()
            id = str(uuid.uuid4())
            vendor_id = user.id
            transactions = get_transactions(rows, id, vendor_id)
            values = ", ".join(map(str, transactions))
            cursor.execute(f'''
                INSERT INTO transactions VALUES {values}
            ''')
        except Exception as exception:
            if cursor is not None:
                cursor.execute("ROLLBACK")
            logger.error(exception)
        finally:
            if cursor is not None:
                cursor.close()
