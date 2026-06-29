import vectorbt as vbt

from strategy.ma_strategy import generate_signals


def run_vectorbt(df):

    entries, exits = generate_signals(df)

    portfolio = vbt.Portfolio.from_signals(

        close=df["Close"],

        entries=entries,

        exits=exits,

        init_cash=10000,

        fees=0.001,

        slippage=0.001,

        freq="1D"

    )

    return portfolio