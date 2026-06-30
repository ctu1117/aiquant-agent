import pandas as pd

def analyze_technical(df:pd.DataFrame):
    latest=df.iloc[-1]
    result={}

    #趋势
    if latest["MA20"]>latest["MA60"]:
        result["trend"]="UP"
    else:
        result["trend"]="DOWN"
    #RSI
    result["RSI"]=round(latest["RSI"],2)

    if latest["RSI"] > 70:
        result["rsi_signal"] = "OVERBOUGHT"
    elif latest["RSI"] < 30:
        result["rsi_signal"] = "OVERSOLD"
    else:
        result["rsi_signal"] = "NORMAL"

    # MA信号
    prev = df.iloc[-2]

    if (
        prev["MA20"] <= prev["MA60"]
        and
        latest["MA20"] > latest["MA60"]
    ):
        result["ma_signal"] = "BUY"
    elif (
        prev["MA20"] >= prev["MA60"]
        and
        latest["MA20"] < latest["MA60"]
    ):
        result["ma_signal"] = "SELL"
    else:
        result["ma_signal"] = "HOLD"

    return result
