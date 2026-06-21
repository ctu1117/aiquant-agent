def generate_signal(
    prev_ma20,
    prev_ma60,
    curr_ma20,
    curr_ma60,
    rsi
):

    # 金叉 + RSI不过热
    if (
        prev_ma20 <= prev_ma60
        and curr_ma20 > curr_ma60
    ):

        return "BUY"

    # 死叉
    elif (
        prev_ma20 >= prev_ma60
        and curr_ma20 < curr_ma60
    ):
        return "SELL"

    # RSI极度过热
    elif rsi > 95:
        return "SELL"

    return "HOLD"