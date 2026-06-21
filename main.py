from data_agent import load_data
from backtest.engine import run_backtest
from agent.report_agent import generate_report
from strategy.ma_strategy import generate_signal
from analyze.analyze_agent import analyze_analyze
from agent.market_agent import get_market_data
df = load_data()
final_cash, trades, trade_log = run_backtest(df)
prev_ma20 = df["MA20"].iloc[-2]
prev_ma60 = df["MA60"].iloc[-2]

curr_ma20 = df["MA20"].iloc[-1]
curr_ma60 = df["MA60"].iloc[-1]

rsi = df["RSI"].iloc[-1]
signal=generate_signal(prev_ma20, prev_ma60, curr_ma20, curr_ma60,rsi)
report=generate_report(signal, curr_ma20, curr_ma60)

print("最终资金:", round(final_cash, 2))
print("交易次数:", trades)
print(report)
print(df[["Close","RSI"]].tail())
print("\n===== 实时行情 =====")
print(get_market_data("NVDA"))

print("\n===== 板块分析 =====")
ranking = analyze_analyze()
print(ranking)