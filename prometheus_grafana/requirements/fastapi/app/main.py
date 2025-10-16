from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
import random
import time
import logging
from login import router as l_router
from products import router as p_router
from transactions import router as t_router

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

app.include_router(p_router)
app.include_router(l_router)
app.include_router(t_router)

Instrumentator().instrument(app).expose(app)

@app.get("/hello")
async def get_hello():
    delay = random.randint(0, 5)
    time.sleep(delay)
    return "Hello World!"
