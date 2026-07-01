import vectorbt as vbt
from config.user_profile import USER_PROFILE
from strategy.ma_strategy import generate_signals

money = USER_PROFILE["money"]
def run_vectorbt(df,money):

    entries, exits = generate_signals(df)

    portfolio = vbt.Portfolio.from_signals(

        close=df["Close"],

        entries=entries,

        exits=exits,

        init_cash=money,

        fees=0.001,

        slippage=0.001,

        freq="1D"

    )

    return portfolio