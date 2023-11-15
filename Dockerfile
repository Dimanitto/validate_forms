FROM python:3.11-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir

COPY . /app

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
