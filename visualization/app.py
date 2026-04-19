from pathlib import Path
import json
import os
import time
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://open_data_user:open_data_password@db:5432/open_data_db")
TABLE_NAME = os.getenv("TABLE_NAME", "transport_data")
SHARED_DIR = Path(os.getenv("SHARED_DIR", "/app/shared"))
OUTPUT_DIR = SHARED_DIR / "figures"
META_FILE = OUTPUT_DIR / "plots.json"

def wait_for_db():
    last_error = None
    for attempt in range(20):
        try:
            engine = create_engine(DB_URL)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
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

    created_files = []

    categorical_columns = df.select_dtypes(include=["object"]).columns.tolist()
    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

    for col in categorical_columns[:2]:
        series = df[col].dropna().astype(str).value_counts().head(10)
        if not series.empty:
            plt.figure(figsize=(10, 6))
            series.sort_values().plot(kind="barh")
            plt.title(f"Top values for {col}")
            plt.xlabel("Count")
            plt.ylabel(col)
            plt.tight_layout()
            filename = f"{col}_top.png"
            plt.savefig(OUTPUT_DIR / filename)
            plt.close()
            created_files.append(filename)

    if numeric_columns:
        col = numeric_columns[0]
        plt.figure(figsize=(10, 6))
        df[col].dropna().plot(kind="hist", bins=20)
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.tight_layout()
        filename = f"{col}_hist.png"
        plt.savefig(OUTPUT_DIR / filename)
        plt.close()
        created_files.append(filename)

    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump({"plots": created_files}, f, ensure_ascii=False, indent=2)

    print(f"Plots saved to: {OUTPUT_DIR}")
    print(json.dumps({"plots": created_files}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
