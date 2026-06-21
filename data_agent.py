import pandas as pd
from strategy.rsi import calculate_rsi
def load_data():

    df = pd.read_csv("data/QQQ.csv")
    df["Close"] = (
        df["Close/Last"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .astype(float)
    )

    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values("Date")

    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA60"] = df["Close"].rolling(60).mean()
    df["RSI"] = calculate_rsi(df)

    return df