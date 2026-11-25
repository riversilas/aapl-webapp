"""Download AAPL daily OHLCV for the past 2 years and save as data/aapl.csv."""

import os
import yfinance as yf


def main():
    # Ensure the output directory exists
    os.makedirs("data", exist_ok=True)

    # Download daily OHLCV for the past 2 years
    df = yf.download(
        "AAPL",
        period="2y",
        auto_adjust=True,
        progress=False,
    )

    # Flatten possible MultiIndex columns from yfinance
    if isinstance(df.columns, tuple) or hasattr(df.columns, "levels"):
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    # Keep standard OHLCV columns
    keep = ["Open", "High", "Low", "Close", "Volume"]
    df = df[[c for c in keep if c in df.columns]].copy()

    # Make Date a real column instead of just the index
    df = df.reset_index()
    df = df.rename(columns=str.capitalize)
    # Ensure the date column is named "Date"
    if "Datetime" in df.columns:
        df = df.rename(columns={"Datetime": "Date"})

    # Drop empty rows and save
    df = df.dropna(how="all")
    out_path = "data/aapl.csv"
    df.to_csv(out_path, index=False)

    # Report
    print(f"Saved {len(df)} rows to {out_path}")
    print(f"Date range: {df['Date'].min()} -> {df['Date'].max()}")
    print()
    print("Column names:")
    print(list(df.columns))
    print()
    print("First 5 rows:")
    print(df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
