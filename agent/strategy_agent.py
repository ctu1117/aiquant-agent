from openai import OpenAI
from settings import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    LLM_MODEL,
    LLM_TEMPERATURE,
)
import json

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)


def make_decision(
    technical: dict,
    market: dict,
    news: dict,
):
    best_sector = market.get("best_sector", market.get("symbol", "未知"))
    market_score = market.get("score", int(round(market.get("change", 0) * 10 + 50)))

    prompt = f"""
你是一名专业量化投资策略分析师。

请根据以下信息判断当前是否适合买入。

=========================
【技术分析】

趋势：
{technical.get("trend", "未知")}

均线信号：
{technical.get("ma_signal", "未知")}

RSI：
{technical.get("RSI", 50)}

RSI状态：
{technical.get("rsi_signal", "未知")}

=========================
【市场分析】

最强板块/标的：
{best_sector}

市场评分：
{market_score}

=========================
【新闻分析】

新闻摘要：
{news["summary"]}

新闻情绪：
{news["sentiment"]}

新闻评分：
{news["score"]}

=========================

请仅返回JSON：

{{
    "signal":"BUY/HOLD/SELL",
    "confidence":90,
    "score":88,
    "reasons":[
        "...",
        "...",
        "..."
    ]
}}

要求：

1 signal只能是 BUY HOLD SELL

2 confidence 为0~100

3 score 为0~100

4 reasons 三条以内

5 不要输出Markdown

6 不要输出解释

7 只返回JSON
"""
        
    response = client.chat.completions.create(
    model=LLM_MODEL,
    messages=[
        {
            "role": "system",
            "content": "你是一名专业量化投资策略分析师，只返回JSON。"
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2
)   

    return json.loads(
        response.choices[0].message.content
    )