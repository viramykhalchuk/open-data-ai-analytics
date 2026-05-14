FROM python:3.11-slim

WORKDIR /app

COPY web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY web/app.py /app/app.py
COPY web/templates /app/templates

RUN mkdir -p /app/shared/quality /app/shared/research /app/shared/figures

CMD ["python", "app.py"]
