from pathlib import Path
import json
import os
import time
import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://open_data_user:open_data_password@db:5432/open_data_db")
TABLE_NAME = os.getenv("TABLE_NAME", "transport_data")
SHARED_DIR = Path(os.getenv("SHARED_DIR", "/app/shared"))
OUTPUT_DIR = SHARED_DIR / "research"
OUTPUT_FILE = OUTPUT_DIR / "research_report.json"

def wait_for_db():
    last_error = None
    for attempt in range(20):
        try:
            engine = create_engine(DB_URL)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready")
            return engine
        except Exception as e:
            last_error = e
            print(f"Waiting for database... attempt {attempt + 1}/20")
            time.sleep(3)
    raise RuntimeError(f"Database is not available: {last_error}")

def make_json_safe(value):
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    return value

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    engine = wait_for_db()
    df = pd.read_sql(f'SELECT * FROM "{TABLE_NAME}"', engine)

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = df.select_dtypes(include=["object"]).columns.tolist()

    numeric_summary = {}
    for col in numeric_columns:
        numeric_summary[col] = {
            "mean": make_json_safe(df[col].mean()),
            "median": make_json_safe(df[col].median()),
            "min": make_json_safe(df[col].min()),
            "max": make_json_safe(df[col].max())
        }

    categorical_summary = {}
    for col in categorical_columns[:5]:
        top_values = df[col].astype(str).value_counts(dropna=False).head(5).to_dict()
        categorical_summary[col] = {str(k): int(v) for k, v in top_values.items()}

    report = {
        "table_name": TABLE_NAME,
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "numeric_summary": numeric_summary,
        "categorical_top_values": categorical_summary
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Research report saved to: {OUTPUT_FILE}")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
