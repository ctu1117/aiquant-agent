def generate_report(signal,ma20,ma60):
    if signal=="BUY":
        return f"""
===== 市场分析报告 =====

MA20: {ma20:.2f}
MA60: {ma60:.2f}

短期均线高于长期均线。

系统检测到金叉信号。

市场可能进入上涨趋势。

建议操作：BUY
"""

    elif signal == "SELL":

        return f""" 
===== 市场分析报告 =====
MA20: {ma20:.2f}
MA60: {ma60:.2f}

短期均线低于长期均线。

系统检测到死叉信号。

市场可能进入下跌趋势。

建议操作：SELL
"""

    return f"""
===== 市场分析报告 =====
MA20: {ma20:.2f}
MA60: {ma60:.2f}

当前没有出现新的交易信号。

建议继续观察市场。

建议操作：HOLD
"""