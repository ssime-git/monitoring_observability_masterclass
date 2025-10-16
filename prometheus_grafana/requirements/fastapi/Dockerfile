FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

COPY ./app/requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./app/main.py .

ENTRYPOINT [ "uvicorn", "main:app" ]
