FROM python:3-slim

EXPOSE 8080
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

CMD uvicorn main:app
