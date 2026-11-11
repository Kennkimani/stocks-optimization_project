"""Load and prepare historical adjusted-close price data."""
from pathlib import Path
import pandas as pd


def load_prices(path: str | Path, date_column: str = "Date") -> pd.DataFrame:
    """Load a CSV of prices; return a sorted DateTimeIndex x asset DataFrame."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Price data not found: {path}. Add stocks_data.csv to data/.")
    frame = pd.read_csv(path)
    if date_column not in frame.columns:
        # Handle the common CSV export format where the date index was saved unnamed.
        unnamed = [c for c in frame.columns if str(c).startswith("Unnamed:")]
        if not unnamed:
            raise ValueError(f"Expected a '{date_column}' column or an unnamed date column.")
        frame = frame.rename(columns={unnamed[0]: date_column})
    frame[date_column] = pd.to_datetime(frame[date_column], errors="coerce")
    frame = frame.dropna(subset=[date_column]).set_index(date_column).sort_index()
    frame = frame.apply(pd.to_numeric, errors="coerce")
    frame = frame.dropna(axis=1, how="all").dropna(how="all")
    if frame.empty:
        raise ValueError("No usable price observations found in the CSV.")
    if (frame <= 0).any().any():
        raise ValueError("Prices must be positive; inspect the source data.")
    return frame


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate simple daily returns, retaining the initial NaN row."""
    return prices.pct_change(fill_method=None)
