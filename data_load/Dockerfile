FROM python:3.11-slim

WORKDIR /app

COPY data_load/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data_load/app.py /app/app.py
COPY data /app/data
COPY shared /app/shared

CMD ["python", "app.py"]
