from pathlib import Path
import json
import os
import time
import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://open_data_user:open_data_password@db:5432/open_data_db")
TABLE_NAME = os.getenv("TABLE_NAME", "transport_data")
SHARED_DIR = Path(os.getenv("SHARED_DIR", "/app/shared"))
OUTPUT_DIR = SHARED_DIR / "quality"
OUTPUT_FILE = OUTPUT_DIR / "quality_report.json"

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

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    engine = wait_for_db()
    df = pd.read_sql(f'SELECT * FROM "{TABLE_NAME}"', engine)

    report = {
        "table_name": TABLE_NAME,
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values_total": int(df.isna().sum().sum()),
        "missing_by_column": {col: int(val) for col, val in df.isna().sum().to_dict().items()},
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.to_dict().items()},
        "non_null_by_column": {col: int(val) for col, val in df.notna().sum().to_dict().items()}
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Quality report saved to: {OUTPUT_FILE}")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
