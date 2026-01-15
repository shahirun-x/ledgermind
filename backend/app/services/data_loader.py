import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

TRADES_PATH = DATA_DIR / "trades.csv"
HOLDINGS_PATH = DATA_DIR / "holdings.csv"


def load_trades():
    df = pd.read_csv(TRADES_PATH)
    validate_schema(df, TRADES_REQUIRED_COLUMNS)
    return df


def load_holdings():
    df = pd.read_csv(HOLDINGS_PATH)
    validate_schema(df, HOLDINGS_REQUIRED_COLUMNS)
    return df


from app.core.schemas import (
    TRADES_REQUIRED_COLUMNS,
    HOLDINGS_REQUIRED_COLUMNS,
)


def validate_schema(df, required_columns: set):
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
