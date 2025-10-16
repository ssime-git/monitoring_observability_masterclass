FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

COPY ./app/requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app .

# Clear Python cache and enable hot reloading
RUN find . -type d -name __pycache__ -exec rm -r {} +
