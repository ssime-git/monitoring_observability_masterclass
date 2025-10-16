from fastapi import APIRouter, Depends
from login import manager
from logger import logger
import time
from postgres import connect_psql

router = APIRouter(
    prefix="/deadlock",
    tags=["deadlock"]
)

@router.put("/put1")
async def put1(user=Depends(manager)):
    with connect_psql() as conn:
        try:
            cursor = conn.cursor()
            logger.debug(f'{user.username} : executing products1 query 1')
            cursor.execute('''
                    UPDATE products
                    SET price = price + 1
                    WHERE id = 'a24984cb-e42f-49a4-9ee4-508dc5466f5f'
                    ''')
            time.sleep(6)
            logger.debug(f'{user.username} : executing products1 query 2')
            cursor.execute('''
                    UPDATE products
                    SET price = price + 1
                    WHERE id = '80fd7bb5-1d6b-446e-a047-7b96004a072e'
                    ''')
            user.conn_psql.commit()
        except Exception as exception:
            if cursor is not None:
                cursor.execute("ROLLBACK")
                return exception
        finally:
            if cursor is not None:
                cursor.close()

@router.put("/put2")
async def put2(user=Depends(manager)):
    with connect_psql() as conn:
        try:
            cursor = conn.cursor()
            logger.debug(f'{user.username} : executing products1 query 1')
            cursor.execute('''
                    UPDATE products
                    SET price = price + 2
                    WHERE id = '80fd7bb5-1d6b-446e-a047-7b96004a072e'
                    ''')
            time.sleep(6)
            logger.debug(f'{user.username} : executing products1 query 2')
            cursor.execute('''
                    UPDATE products
                    SET price = price + 2
                    WHERE id = 'a24984cb-e42f-49a4-9ee4-508dc5466f5f'
                    ''')
            user.conn_psql.commit()
        except Exception as exception:
            if cursor is not None:
                cursor.execute("ROLLBACK")
                return exception
        finally:
            if cursor is not None:
                cursor.close()
