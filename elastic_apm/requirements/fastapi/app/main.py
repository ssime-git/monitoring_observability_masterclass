from fastapi import FastAPI
from pydantic import BaseModel
import random
import time
import logging
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from login import router as l_router
from products import router as p_router
from transactions import router as t_router
from deadlock import router as d_router
from apm import router as apm_router, apm_client

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

# Initialize the APM client
app.add_middleware(ElasticAPM, client=apm_client)

# Include routers
app.include_router(l_router)
app.include_router(p_router)
app.include_router(t_router)
app.include_router(d_router)
app.include_router(apm_router)

@app.get("/")
def get_hello():
    return {"message": "Hello World"}
