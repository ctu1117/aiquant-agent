from agent.data_agent import load_data
from backtest.vectorbt import run_vectorbt
from strategy.ma_strategy import generate_signals
from agent.data_agent import load_data
df=load_data()
entries, exits = generate_signals(df)

print("买入次数：", entries.sum())
print("卖出次数：", exits.sum())
df = load_data("QQQ")

portfolio = run_vectorbt(df)

print(portfolio.stats())
cross = (
    (df["MA20"] > df["MA60"]) &
    (df["MA20"].shift(1) <= df["MA60"].shift(1))
)

print("金叉次数：", cross.sum())