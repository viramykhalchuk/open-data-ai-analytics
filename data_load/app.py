from pathlib import Path
import os
import re
import time
import pandas as pd
from sqlalchemy import create_engine, text

CSV_PATH = Path(os.getenv("CSV_PATH", "/app/data/demo/transport_demo.csv"))
DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://open_data_user:open_data_password@db:5432/open_data_db")
TABLE_NAME = os.getenv("TABLE_NAME", "transport_data")

def normalize_column_name(name: str) -> str:
    value = str(name).strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    if not value:
        value = "column"
    return value

def read_csv_smart(path: Path) -> pd.DataFrame:
    return pd.read_csv(
        path,
        sep=None,
        engine="python",
        encoding="utf-8",
        encoding_errors="replace",
        on_bad_lines="skip"
    )

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
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    df = read_csv_smart(CSV_PATH)
    df.columns = [normalize_column_name(col) for col in df.columns]

    engine = wait_for_db()

    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False, chunksize=1000)

    with engine.connect() as conn:
        row_count = conn.execute(text(f'SELECT COUNT(*) FROM "{TABLE_NAME}"')).scalar()

    print(f"Loaded table: {TABLE_NAME}")
    print(f"Rows loaded: {row_count}")
    print(f"Columns: {list(df.columns)}")

if __name__ == "__main__":
    main()
