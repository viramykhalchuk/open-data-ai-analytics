from pathlib import Path
import pandas as pd

PATH = Path("data/processed/sample_head.csv")

def main():
    if not PATH.exists():
        raise FileNotFoundError("Немає data/processed/sample_head.csv. Спочатку запусти: python3 src/data_load.py --rows 5000")

    df = pd.read_csv(PATH, low_memory=False)

    print("shape:", df.shape)
    print("columns:", list(df.columns))

    missing = df.isna().sum().sort_values(ascending=False)
    print("\nmissing_top:")
    print(missing.head(20))

    print("\nduplicates:", int(df.duplicated().sum()))
    print("\ndtypes:")
    print(df.dtypes)

    if not df.select_dtypes(include="number").empty:
        print("\nnumeric_describe:")
        print(df.select_dtypes(include="number").describe().transpose().head(20))

if __name__ == "__main__":
    main()
