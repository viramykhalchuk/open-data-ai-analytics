from pathlib import Path
import argparse

def make_sample(inp: Path, out: Path, rows: int) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with inp.open("r", encoding="utf-8", errors="replace") as f_in, out.open("w", encoding="utf-8", newline="") as f_out:
        header = f_in.readline()
        if not header:
            raise ValueError("Empty file")
        f_out.write(header)
        for line in f_in:
            f_out.write(line)
            n += 1
            if n >= rows:
                break

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="data/raw/dataser.csv")
    p.add_argument("--rows", type=int, default=5000)
    p.add_argument("--output", default="data/processed/sample_head.csv")
    args = p.parse_args()

    inp = Path(args.input)
    out = Path(args.output)

    if not inp.exists():
        raise FileNotFoundError(f"Not found: {inp}")

    make_sample(inp, out, args.rows)
    print(f"Saved sample to: {out}")

if __name__ == "__main__":
    main()
