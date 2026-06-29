from strategy.ma_strategy import generate_signal


def run_backtest(df, initial_cash=10000):

    cash = initial_cash
    shares = 0

    trade_count = 0

    trade_log = []

    equity_curve = []

    for i in range(60, len(df)):

        date = df["Date"].iloc[i]
        price = df["Close"].iloc[i]

        prev_ma20 = df["MA20"].iloc[i - 1]
        prev_ma60 = df["MA60"].iloc[i - 1]

        curr_ma20 = df["MA20"].iloc[i]
        curr_ma60 = df["MA60"].iloc[i]

        rsi = df["RSI"].iloc[i]

        signal = generate_signal(
            prev_ma20,
            prev_ma60,
            curr_ma20,
            curr_ma60,
            rsi
        )

        # ===========================
        # BUY
        # ===========================
        if signal == "BUY" and shares == 0:

            shares = cash / price
            cash = 0

            trade_count += 1

            trade_log.append({

                "date": date,

                "action": "BUY",

                "price": round(price, 2),

                "shares": round(shares, 4),

                "cash": round(cash, 2)

            })

        # ===========================
        # SELL
        # ===========================
        elif signal == "SELL" and shares > 0:

            cash = shares * price

            trade_count += 1

            trade_log.append({

                "date": date,

                "action": "SELL",

                "price": round(price, 2),

                "shares": round(shares, 4),

                "cash": round(cash, 2)

            })

            shares = 0

        # ===========================
        # 每日资产
        # ===========================
        equity = cash + shares * price

        equity_curve.append({

            "date": date,

            "equity": round(equity, 2)

        })

    # ===========================
    # 最后一天强制平仓
    # ===========================
    if shares > 0:

        final_price = df["Close"].iloc[-1]
        final_date = df["Date"].iloc[-1]

        cash = shares * final_price

        trade_count += 1

        trade_log.append({

            "date": final_date,

            "action": "FORCE SELL",

            "price": round(final_price, 2),

            "shares": round(shares, 4),

            "cash": round(cash, 2)

        })

        shares = 0

    # ===========================
    # 返回结果
    # ===========================
    result = {

        "initial_cash": initial_cash,

        "final_cash": round(cash, 2),

        "profit": round(cash - initial_cash, 2),

        "return_pct": round((cash / initial_cash - 1) * 100, 2),

        "trade_count": trade_count,

        "trade_log": trade_log,

        "equity_curve": equity_curve

    }

    return result