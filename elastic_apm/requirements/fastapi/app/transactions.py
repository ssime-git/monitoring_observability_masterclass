from fastapi import APIRouter, Depends, HTTPException
from login import manager
from logger import logger
from pydantic import BaseModel
import uuid
from postgres_2 import get_db_connection, put_db_connection
from elasticapm.traces import capture_span

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
    with capture_span("get-transactions", "db.postgresql.query"):
        key = str(uuid.uuid4())
        conn = get_db_connection(key)
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM transactions''')
            result = cursor.fetchall()
            conn.commit()
            return result
        except Exception as exception:
            if cursor is not None:
                cursor.execute("ROLLBACK")
                logger.error(exception)
            raise
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                put_db_connection(conn, key)

@router.post("")
async def post_transaction(transaction: Transaction, user=Depends(manager)):
    with capture_span("post-transaction", "db.postgresql.query"):
        key = str(uuid.uuid4())
        conn = get_db_connection(key)
        cursor = None
        try:
            cursor = conn.cursor()
            # Check if enough products are available
            cursor.execute(
                '''SELECT quantity >= %s FROM products WHERE id = %s FOR NO KEY UPDATE''',
                (transaction.quantity, transaction.product_id)
            )
            result = cursor.fetchone()
            if not result or not result[0]:
                raise HTTPException(status_code=422, detail=f"Not enough products {transaction.product_id}")
            
            logger.debug(f"Product {transaction.product_id} available")
            
            # Update product quantity
            cursor.execute(
                '''UPDATE products SET quantity = quantity - %s WHERE id = %s''',
                (transaction.quantity, transaction.product_id)
            )
            logger.debug(f"Product {transaction.product_id} quantity updated")
            
            # Insert transaction
            cursor.execute(
                '''INSERT INTO transactions (id, product_id, vendor_id, action, quantity) VALUES (%s, %s, %s, %s, %s)''',
                (transaction.id, transaction.product_id, transaction.vendor_id, transaction.action, transaction.quantity)
            )
            conn.commit()
            return f"Transaction {transaction.id} inserted"
        except Exception as exception:
            if cursor is not None:
                cursor.execute("ROLLBACK")
                logger.error(f"Transaction error: {str(exception)}")
            raise HTTPException(status_code=500, detail=str(exception))
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                put_db_connection(conn, key)
