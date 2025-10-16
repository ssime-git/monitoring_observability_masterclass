from fastapi import APIRouter, Depends, HTTPException
from login import manager
from logger import logger
from pydantic import BaseModel
import uuid
from postgres import connect_psql

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

class Transaction(BaseModel):
    id: str
    product_id: str
    vendor_id: str
    action: str
    quantity: int

@router.get("")
async def get_transactions(user=Depends(manager)):
    with connect_psql() as conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM transactions''')
            result = cursor.fetchall()
            conn.commit()
        except Exception as exception:
            if cursor is not None:
                cursor.execute("ROLLBACK")
                logger.error(exception)
            raise
        finally:
            if cursor is not None:
                cursor.close()
            return result

@router.post("")
async def post_transaction(transaction: Transaction, user=Depends(manager)):
    with connect_psql() as conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT quantity > {transaction.quantity} FROM products
                WHERE id = '{transaction.product_id}'
                FOR NO KEY UPDATE
            ''')
            is_available = cursor.fetchone()[0]
            if not is_available:
                cursor.execute("ROLLBACK")
                raise HTTPException(status_code=422, detail=f"Not enough products {transaction.product_id}")
            logger.debug(f"Product {transaction.product_id} available")
            cursor.execute(f'''
                UPDATE products
                SET quantity = quantity - {transaction.quantity}
                WHERE id = '{transaction.product_id}'
            ''')
            logger.debug(f"Product {transaction.product_id} quantity updated")
            cursor.execute(f'''
                INSERT INTO transactions(id, product_id, vendor_id, action, quantity) VALUES
                ('{transaction.id}', '{transaction.product_id}', '{transaction.vendor_id}', '{transaction.action}', {transaction.quantity});
            ''')
            conn.commit()
            return f"Transaction {transaction.id} inserted"
        except Exception as exception:
            if cursor is not None:
                cursor.execute("ROLLBACK")
                logger.error(exception)
            raise
        finally:
            if cursor is not None:
                cursor.close()
