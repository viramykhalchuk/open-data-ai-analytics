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
        raise FileNotFoundError("Немає data/processed/sample_head.csv. Спочатку запусти: python3 src/data_load.py --rows 5000")

    df = read_csv_smart(PATH)

    print("shape:", df.shape)
    print("columns:", list(df.columns))

    missing = df.isna().sum().sort_values(ascending=False)
    print("\nmissing_top:")
    print(missing.head(20))

    print("\nduplicates:", int(df.duplicated().sum()))
    print("\ndtypes:")
    print(df.dtypes)

    num = df.select_dtypes(include="number")
    if not num.empty:
        print("\nnumeric_describe:")
        print(num.describe().transpose().head(20))

if __name__ == "__main__":
    main()
