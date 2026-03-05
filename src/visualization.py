from pathlib import Path
import csv
import pandas as pd
import matplotlib.pyplot as plt

PATH = Path("data/processed/sample_head.csv")
OUT_DIR = Path("reports/figures")

def read_csv_smart(path: Path) -> pd.DataFrame:
    with path.open("r", encoding="utf-8", errors="replace") as f:
        sample = f.read(4096)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        sep = dialect.delimiter
    except csv.Error:
        sep = ","
    df = pd.read_csv(path, sep=sep, engine="python", on_bad_lines="skip")
    print("detected_sep:", repr(sep))
    return df

def save_bar(series: pd.Series, title: str, filename: str) -> None:
    plt.figure(figsize=(10, 6))
    series.plot(kind="bar")
    plt.title(title)
    plt.xlabel("")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUT_DIR / filename, dpi=150)
    plt.close()

def save_hist(series: pd.Series, title: str, filename: str) -> None:
    plt.figure(figsize=(10, 6))
    series.dropna().plot(kind="hist", bins=20)
    plt.title(title)
    plt.xlabel(series.name)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(OUT_DIR / filename, dpi=150)
    plt.close()

def main():
    if not PATH.exists():
        raise FileNotFoundError("Немає data/processed/sample_head.csv. Запусти: python3 src/data_load.py --rows 5000")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = read_csv_smart(PATH)

    if "BRAND" in df.columns:
        save_bar(df["BRAND"].astype(str).value_counts().head(10), "Top 10 brands", "top_brands.png")

    if "FUEL" in df.columns:
        save_bar(df["FUEL"].astype(str).value_counts().head(10), "Fuel types", "fuel_types.png")

    if "COLOR" in df.columns:
        save_bar(df["COLOR"].astype(str).value_counts().head(10), "Top 10 colors", "top_colors.png")

    if "MAKE_YEAR" in df.columns:
        years = pd.to_numeric(df["MAKE_YEAR"], errors="coerce")
        save_hist(years, "Distribution of make year", "make_year_hist.png")

    print("Saved figures to:", OUT_DIR)

if __name__ == "__main__":
    main()
