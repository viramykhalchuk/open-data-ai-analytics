from pathlib import Path
from time import time
import json
import os
import pandas as pd
from flask import Flask, Response, g, render_template, request, send_from_directory
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from sqlalchemy import create_engine

DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://open_data_user:open_data_password@db:5432/open_data_db")
TABLE_NAME = os.getenv("TABLE_NAME", "transport_data")
SHARED_DIR = Path(os.getenv("SHARED_DIR", "/app/shared"))

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "open_data_web_requests_total",
    "Total number of HTTP requests processed by the web service",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "open_data_web_request_duration_seconds",
    "HTTP request latency of the web service",
    ["endpoint"],
)

APP_INFO = Gauge(
    "open_data_web_app_info",
    "Information metric showing that the Open Data AI Analytics web app is running",
    ["service"],
)
APP_INFO.labels(service="web").set(1)


def load_json(path: Path):
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.before_request
def before_request():
    g.start_time = time()


@app.after_request
def after_request(response):
    endpoint = request.path
    REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
    REQUEST_LATENCY.labels(endpoint).observe(time() - getattr(g, "start_time", time()))
    return response


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/health")
def health():
    return {"status": "ok", "service": "web"}


@app.route("/figures/<path:filename>")
def figures(filename):
    return send_from_directory(SHARED_DIR / "figures", filename)


@app.route("/")
def index():
    quality_report = load_json(SHARED_DIR / "quality" / "quality_report.json")
    research_report = load_json(SHARED_DIR / "research" / "research_report.json")

    preview_columns = []
    preview_rows = []
    db_error = None

    try:
        engine = create_engine(DB_URL)
        preview_df = pd.read_sql(f'SELECT * FROM "{TABLE_NAME}" LIMIT 10', engine)
        preview_columns = preview_df.columns.tolist()
        preview_rows = preview_df.fillna("").astype(str).to_dict(orient="records")
    except Exception as e:
        db_error = str(e)

    figure_files = sorted([p.name for p in (SHARED_DIR / "figures").glob("*.png")])

    return render_template(
        "index.html",
        preview_columns=preview_columns,
        preview_rows=preview_rows,
        db_error=db_error,
        quality_report=quality_report,
        research_report=research_report,
        figure_files=figure_files,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
