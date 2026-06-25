from data_agent import load_data
from backtest.engine import run_backtest
from agent.report_agent import generate_report
from strategy.ma_strategy import generate_signal
from analyze.analyze_agent import analyze_analyze
from agent.market_agent import get_market_data
from agent.advisor_agent import generate_advice
from config.user_profile import USER_PROFILE
from agent.llm_agent import generate_llm_report
from agent.news_summary_agent import summarize_news 
from agent.news_agent import get_news

df = load_data()
final_cash, trades, trade_log = run_backtest(df)
prev_ma20 = df["MA20"].iloc[-2]
prev_ma60 = df["MA60"].iloc[-2]

curr_ma20 = df["MA20"].iloc[-1]
curr_ma60 = df["MA60"].iloc[-1]

rsi = df["RSI"].iloc[-1]
signal=generate_signal(prev_ma20, prev_ma60, curr_ma20, curr_ma60,rsi)
report=generate_report(signal, curr_ma20, curr_ma60)

money = USER_PROFILE["money"]
risk = USER_PROFILE["risk"]


news = get_news("NVDA", days=7, limit=15)

print("最终资金:", round(final_cash, 2))
print("交易次数:", trades)
print(report)
print(df[["Close","RSI"]].tail())
print("\n===== 实时行情 =====")
print(get_market_data("NVDA"))

print("\n===== 板块分析 =====")

ranking = analyze_analyze()

for item in ranking:#遍历每个行业的分析结果

    print(
        f"{item['sector']} : "
        f"{item['avg_change']}%"
    )
print("\n===== 投资建议 =====")
advice = generate_advice(ranking,money,risk) 
print(advice)


print("\n===== LLM 投资建议 =====")
llm_report = generate_llm_report(ranking, money, risk, news)
print(llm_report)


print("\n===== 新闻 =====")
summary = summarize_news(news)
print(summary)