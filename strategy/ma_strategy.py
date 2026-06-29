import pandas as pd

def generate_signals(df:pd.DataFrame):
    entries=(
        (df["MA20"]>df["MA60"])
        &
        (df["MA20"].shift(1)<=df["MA60"].shift(1))
        &
        (df["RSI"]<70)
    )
    exits=(    
        (df["MA20"] < df["MA60"])
        &
        (df["MA20"].shift(1) >= df["MA60"].shift(1))
    )
    return entries.fillna(False), exits.fillna(False)