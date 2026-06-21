from strategy.ma_strategy import generate_signal


def run_backtest(df):

    cash = 10000
    shares = 0

    trades = 0
    trade_log = []

    for i in range(60, len(df)):
        price = df["Close"].iloc[i]
        prev_ma20 = df["MA20"].iloc[i - 1]
        prev_ma60 = df["MA60"].iloc[i - 1]
        curr_ma20 = df["MA20"].iloc[i]
        curr_ma60 = df["MA60"].iloc[i]
        rsi=df["RSI"].iloc[i]
        signal = generate_signal(prev_ma20, prev_ma60, curr_ma20, curr_ma60,rsi)



        if signal == "BUY" and shares == 0:

            shares = cash / price
            cash = 0
            trades += 1
            trade_log.append(f"Day{i} BUY @ {price}")

        elif signal == "SELL" and shares > 0:

            cash = shares * price
            shares = 0
            trade_log.append(f"Day{i} SELL @ {price}")
            trades += 1

    if shares > 0:
        cash = shares * df["Close"].iloc[-1]

    return cash, trades,trade_log