from fastapi import APIRouter
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
import time
import elasticapm

router = APIRouter(
    prefix="/apm",
    tags=["apm"]
)

apm_config = {
    'SERVICE_NAME': 'fastapi',
    'SECRET_TOKEN': '',
    'SERVER_URL': 'http://apm-server:8200',
    'ENVIRONMENT': 'production',
    'INSTRUMENT_SQLALCHEMY': True,  # Enable SQLAlchemy instrumentation
    'TRANSACTIONS_IGNORE_PATTERNS': ['(?i)^/metrics'],  # Ignore metrics endpoint
    'CAPTURE_BODY': 'all',  # Capture request bodies
    'CAPTURE_HEADERS': True,  # Capture HTTP headers
    'TRANSACTION_MAX_SPANS': 500,  # Maximum number of spans per transaction
    'TRANSACTION_SAMPLE_RATE': 1.0,  # Sample all transactions
}

apm_client = make_apm_client(apm_config)

# Instrument SQLAlchemy
elasticapm.instrument()

@router.get("/")
async def read_root():
    return {"message": "Hello World"}

@router.get("/calculate/{number}")
async def calculate(number: int):
    time.sleep(2)
    result = number * 2
    return {"original": number, "result": result}
