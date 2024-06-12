FROM python:3.11

WORKDIR /webapi

COPY requirements.txt .
COPY .env .
COPY app ./app

RUN pip install -r requirements.txt

EXPOSE 8000
CMD [ "fastapi", "run", "app/main.py"]
