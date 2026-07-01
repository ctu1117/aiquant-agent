from agent.data_agent import load_data
from agent.technical_agent import analyze_technical
from agent.market_agent import get_market_data
from agent.news_agent import get_news
from agent.news_summary_agent import summarize_news
from agent.strategy_agent import make_decision
from backtest.vectorbt import run_vectorbt
from agent.advisor_agent import generate_advice
def run_pipeline(
    symbol,
    money,
    risk
):

    df = load_data(symbol,30)

    technical = analyze_technical(df)

    market = get_market_data(symbol)

    news = get_news(symbol,7,15)

    news_result = summarize_news(news)

    decision = make_decision(
       technical,
       market,
       news_result
    )

    portfolio = run_vectorbt(df, money)

    advice = generate_advice(
        market,
        decision,
        money,
        risk,
        news=news_result,
    )

    return {
        "symbol": symbol,
        "technical": technical,
        "market": market,
        "news": news_result,
        "decision": decision,
        "portfolio": portfolio,
        "report": advice
    }