# data_agent.py
import pandas as pd
from polygon import RESTClient
from strategy.rsi import calculate_rsi
from settings import POLYGON_API_KEY


def load_data(symbol: str = "QQQ", days: int = 500) -> pd.DataFrame:
    if not POLYGON_API_KEY:
        raise ValueError("POLYGON_API_KEY is not set")

    client = RESTClient(api_key=POLYGON_API_KEY)

    from datetime import date, timedelta
    end_date   = date.today()
    start_date = end_date - timedelta(days=days)

    aggs = client.get_aggs(
        ticker    = symbol,
        multiplier= 1,
        timespan  = "day",
        from_     = str(start_date),
        to        = str(end_date),
        limit     = 50000
    )

    df = pd.DataFrame([{
        "Date":   pd.to_datetime(a.timestamp, unit="ms"),
        "Open":   a.open,
        "High":   a.high,
        "Low":    a.low,
        "Close":  a.close,
        "Volume": a.volume,
    } for a in aggs])

    df = df.sort_values("Date").reset_index(drop=True)
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA60"] = df["Close"].rolling(60).mean()
    df["RSI"]  = calculate_rsi(df)

    return df