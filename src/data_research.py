from pathlib import Path
import csv
import pandas as pd

PATH = Path("data/processed/sample_head.csv")

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

def main():
    if not PATH.exists():
        raise FileNotFoundError("Немає data/processed/sample_head.csv. Запусти: python3 src/data_load.py --rows 5000")

    df = read_csv_smart(PATH)

    print("shape:", df.shape)
    print("\nhead:")
    print(df.head(5))

    print("\nunique_counts (selected):")
    for col in ["KIND", "BODY", "FUEL", "COLOR", "DEP", "BRAND", "MODEL", "PURPOSE"]:
        if col in df.columns:
            print(col, "->", int(df[col].nunique(dropna=True)))

    if "MAKE_YEAR" in df.columns:
        year = pd.to_numeric(df["MAKE_YEAR"], errors="coerce")
        print("\nMAKE_YEAR summary:")
        print(year.describe())

    for col in ["BRAND", "FUEL", "KIND", "COLOR"]:
        if col in df.columns:
            print(f"\nTop values: {col}")
            print(df[col].astype(str).value_counts().head(10))

    numeric_cols = [c for c in ["CAPACITY", "OWN_WEIGHT", "TOTAL_WEIGHT"] if c in df.columns]
    if len(numeric_cols) >= 2:
        num = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
        print("\ncorrelation:")
        print(num.corr(numeric_only=True))

if __name__ == "__main__":
    main()
